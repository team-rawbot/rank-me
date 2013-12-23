from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class TeamManager(models.Manager):
    def get_score_board(self):
        return self.get_query_set().order_by('-score')

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
    users = models.ManyToManyField(User, related_name='teams')
    score = models.IntegerField(default=1000)
    stdev = models.FloatField('standard deviation', default=50)

    objects = TeamManager()

    def __unicode__(self):
        return u" / ".join([user.username for user in self.users.all()])


class GameManager(models.Manager):
    def get_latest(self):
        return self.get_query_set().order_by('-date')[:20]

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
