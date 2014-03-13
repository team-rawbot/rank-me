import operator
import json
import six
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
    score = models.FloatField('skills', default=settings.GAME_INITIAL_MU)
    stdev = models.FloatField('standard deviation',
                              default=settings.GAME_INITIAL_SIGMA)
    wins = models.IntegerField(default=0)
    defeats = models.IntegerField(default=0)

    objects = TeamManager()

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
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

        HistoricalScore.objects.create(
            game=self,
            winner_score=winner.score,
            loser_score=loser.score,
        )

    def get_opponent(self, team):
        """
        Return the opponent team relative to the given team.
        """
        return self.winner if self.winner_id != team.id else self.loser


class HistoricalScoreManager(models.Manager):
    def get_latest(self, nb_games=50):
        return (self.get_queryset()
                .select_related('game', 'game__winner', 'game__loser')
                .order_by('-id')[:nb_games])

    def get_latest_results_by_team(self, nb_games=50, format=''):
        """
        Get nb_games latest scores for each team

        :param nb_games:int number of games
        :param format:string [''/'json']
        :return:dict Dict with key=team and value=list of score objects

        {team_a: [{skill: xx, played: xx, game: game_id}, ...]}
        """
        scores_by_team = {}

        teams = Team.objects.all().select_related('winner', 'loser')

        scores = self.get_latest(nb_games)
        scores = sorted(scores, key=lambda score: score.id)
        for score in scores:
            all_skills_by_game = {}
            for team in teams:
                team_scores = scores_by_team.get(team, [])

                result = {'game': score.game.id}

                if team.id == score.game.winner_id:
                    result['skill'] = score.winner_score
                    result['win'] = True
                    result['played'] = True
                elif team.id == score.game.loser_id:
                    result['skill'] = score.loser_score
                    result['win'] = False
                    result['played'] = True
                else:
                    result['played'] = False
                    if len(team_scores) == 0:
                        result['skill'] = self.get_last_score_for_team(team, scores[0].game)
                    else:
                        result['skill'] = team_scores[-1]['skill']

                all_skills_by_game[team] = result['skill']

                team_scores.append(result)
                scores_by_team[team] = team_scores

            positions_for_game = sorted(six.iteritems(all_skills_by_game), key=operator.itemgetter(1), reverse=True)
            for idx, position in enumerate(positions_for_game, start=1):
                scores_by_team[position[0]][-1]['position'] = idx

        if format == 'json':
            json_result = {}
            for team, results in scores_by_team.items():
                json_result[team.get_name()] = results

            return json.dumps(json_result)

        return scores_by_team

    def get_last_score_for_team(self, team, game):
        """
        Returns the latest skill before game :game for team :team

        :param team:Team
        :param game:Game
        :return:float skill
        """
        historical_score_id = game.historical_score.id
        last_score = (self.get_queryset()
                      .filter(Q(game__winner=team) | Q(game__loser=team))
                      .filter(id__lte=historical_score_id)
                      .select_related('game__winner', 'game__loser', 'game')
                      .order_by('-id')
                      .first())

        if last_score is None:
            return settings.GAME_INITIAL_MU

        return last_score.winner_score if last_score.game.winner == team else last_score.loser_score


class HistoricalScore(models.Model):
    game = models.OneToOneField(Game, related_name='historical_score')
    winner_score = models.FloatField('Winner current score')
    loser_score = models.FloatField('Loser current score')

    objects = HistoricalScoreManager()
