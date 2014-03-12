from collections import OrderedDict
from itertools import groupby

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models import Q

from trueskill import Rating, rate_1vs1


class TeamManager(models.Manager):
    def get_score_board(self):
        return (self.get_query_set().order_by('-score')
                .prefetch_related('users'))

    def get_or_create_from_players(self, player_ids):
        """
        Return the team associated to the given players, creating it first if
        it doesn't exist.

        Args:
            player_ids: a tuple of user ids, or a single user id.
        """
        if not isinstance(player_ids, tuple):
            player_ids = (player_ids,)

        # We need to get only the teams that have the exact number of player
        # ids, otherwise we would also get teams that have the given players
        # plus additional ones
        team = self.annotate(c=models.Count('users')).filter(c=len(player_ids))

        # Chain filter over all player ids
        for player_id in player_ids:
            team = team.filter(users=player_id)

        if not team:
            created = True
            team = self.create()

            for player_id in player_ids:
                team.users.add(player_id)
        else:
            created = False
            team = team.get()

        return (team, created)


class Team(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='teams')
    score = models.FloatField('skills', default=25)
    stdev = models.FloatField('standard deviation', default=8.33)
    wins = models.IntegerField(default=0)
    defeats = models.IntegerField(default=0)

    objects = TeamManager()

    def __unicode__(self):
        return u" / ".join([user.username for user in self.users.all()])

    def get_games(self):
        """
        Fetch the list of games played by the team.
        """
        return (Game.objects.filter(Q(winner_id=self.id) | Q(loser_id=self.id))
                .order_by('-date').select_related('winner', 'loser'))

    def get_head2head(self):
        """
        Compute the amount of wins and defeats against all opponents the team
        played against. The returned value is an OrderedDict since the teams
        are ordered by their score.
        """
        head2head = {}

        games = self.get_games()

        for game in games:
            opponent = game.get_opponent(self)

            if opponent not in head2head:
                head2head[opponent] = {
                    'wins': 0,
                    'defeats': 0,
                    'games': []
                }

            stat_to_increase = (
                'wins' if game.winner_id == self.id else 'defeats'
            )
            head2head[opponent][stat_to_increase] += 1
            head2head[opponent]['games'].append(game)

        return OrderedDict(
            sorted(head2head.items(), key=lambda t: t[0].score, reverse=True)
        )

    def get_recent_stats(self, count=10):
        """
        Return a dictionary with the latest ``count`` played games and the
        number of wins and defeats.
        """
        games = self.get_games()[:count]
        last_games = {
            'wins': 0,
            'defeats': 0,
            'games': []
        }

        for game in games:
            last_games['wins' if game.winner_id == self.id else 'defeats'] += 1
            last_games['games'].append(game)

        return last_games

    def get_longest_streak(self):
        games = self.get_games()
        # Create a list of booleans indicating won matches
        wins_defeats_list = [game.winner_id == self.id for game in games]

        if True in wins_defeats_list:
            # Sum won matches series and keep the max
            return max([sum(g) for k, g in groupby(wins_defeats_list) if k])
        else:
            return 0


class GameManager(models.Manager):
    def get_latest(self):
        return (self.get_query_set()
                .select_related('winner', 'loser')
                .prefetch_related('winner__users', 'loser__users')
                .order_by('-date')[:20])

    def announce(self, winner, loser):
        """
        Announce the results of a new game.

        Args:
            winner: the user id (or tuple of user ids) of the users who won the
            game.
            loser: the user id (or tuple of user ids) of the users who lost the
            game.
        """
        winner, created = Team.objects.get_or_create_from_players(winner)
        loser, created = Team.objects.get_or_create_from_players(loser)

        return self.create(winner=winner, loser=loser)


class Game(models.Model):
    winner = models.ForeignKey(Team, related_name='games_won')
    loser = models.ForeignKey(Team, related_name='games_lost')
    date = models.DateTimeField(default=timezone.now)

    objects = GameManager()

    def clean(self):
        if (self.winner_id is not None and self.loser_id is not None and
                self.winner_id == self.loser_id):
            raise ValidationError(
                "Winner and loser can't be the same team!"
            )

    def __unicode__(self):
        return u"%s beats %s" % (
            self.winner,
            self.loser
        )

    def update_score(self):
        winner = self.winner
        loser = self.loser

        winner_new_score, loser_new_score = rate_1vs1(
            Rating(winner.score, winner.stdev),
            Rating(loser.score, loser.stdev)
        )

        winner.score = winner_new_score.mu
        winner.stdev = winner_new_score.sigma
        winner.wins = winner.wins + 1
        winner.save()

        loser.score = loser_new_score.mu
        loser.stdev = loser_new_score.sigma
        loser.defeats = loser.defeats + 1
        loser.save()

    def get_opponent(self, team):
        """
        Return the opponent team relative to the given team.
        """
        return self.winner if self.winner_id != team.id else self.loser
