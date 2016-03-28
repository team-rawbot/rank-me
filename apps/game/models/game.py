from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from .. import signals
from ..exceptions import InactiveCompetitionError
from .score import update_players_scores


class GameManager(models.Manager):
    def get_latest(self, n):
        games = (self.get_queryset()
                 .select_related('winner', 'loser', 'winner__profile',
                                 'loser__profile')
                 .order_by('-date'))

        games = games[:n]

        return games

    @transaction.atomic
    def announce(self, winner, loser, competition):
        """
        Announce the results of a new game.

        Args:
            winner: the user id (or tuple of user ids) of the users who won the
            game.
            loser: the user id (or tuple of user ids) of the users who lost the
            game.
        """
        if not competition.is_active():
            raise InactiveCompetitionError()

        game = self.create(winner=winner, loser=loser, competition=competition)

        signals.game_played.send(sender=game)
        game.update_score()

        return game


class Game(models.Model):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='games_won')
    loser = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='games_lost')
    date = models.DateTimeField(default=timezone.now)
    competition = models.ForeignKey('Competition', related_name='games')

    objects = GameManager()

    def clean(self):
        if (self.winner_id is not None and self.loser_id is not None and
                self.winner_id == self.loser_id):
            raise ValidationError(
                "Winner and loser can't be the same person!"
            )

    def __str__(self):
        return "[{competition}] {winner} beats {loser}".format(
            competition=self.competition,
            winner=self.winner.profile.get_full_name(),
            loser=self.loser.profile.get_full_name()
        )

    def delete(self):
        """
        Delete the game object and handle related score deletion.
        """
        for player in [self.winner, self.loser]:
            historical_score = self.competition.get_last_score_for_player(
                player, self
            )

            # If the player has a previous score, set its current score to the
            # one before the deleted game. Otherwise, delete its related score
            # since this was its only game in the competition
            if historical_score:
                score = self.competition.get_or_create_score(player)
                score.score = historical_score.score
                score.stdev = historical_score.stdev
                score.save()
            else:
                score = self.competition.get_score(player)
                score.delete()

        self.historical_scores.all().delete()
        super().delete()

    def update_score(self, notify=True):
        """
        Update players scores. This method should be called when a new game is
        created.
        """
        if notify:
            old_rankings = self.competition.get_ranking_by_player()

        update_players_scores(self.winner, self.loser, self)

        if notify:
            new_rankings = self.competition.get_ranking_by_player()

            for player in [self.winner, self.loser]:
                if (player not in old_rankings or
                        old_rankings[player] != new_rankings[player]):
                    signals.ranking_changed.send(
                        sender=self,
                        player=player,
                        old_ranking=(old_rankings[player]
                                     if player in old_rankings else None),
                        new_ranking=new_rankings[player],
                        competition=self.competition
                    )

    def get_opponent(self, player):
        """
        Return the opponent player relative to the given player.
        """
        return self.winner if self.winner_id != player.id else self.loser
