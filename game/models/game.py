from trueskill import Rating, rate_1vs1

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from .. import signals
from ..exceptions import InactiveCompetitionError
from .score import HistoricalScore


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
        return u"%s beats %s" % (
            self.winner,
            self.loser
        )

    def delete(self):
        history_winner = self.competition.get_last_score_for_player(
            self.winner, self
        )
        history_loser = self.competition.get_last_score_for_player(
            self.loser, self
        )

        winner = self.competition.get_or_create_score(self.winner)
        winner.score = history_winner.score
        winner.stdev = history_winner.stdev
        winner.save()

        loser = self.competition.get_or_create_score(self.loser)
        loser.score = history_loser.score
        loser.stdev = history_loser.stdev
        loser.save()

        self.historical_scores.all().delete()
        super().delete()

    def update_score(self, notify=True):
        winner = self.winner
        loser = self.loser
        competition = self.competition

        if notify:
            old_rankings = competition.get_ranking_by_player()

        winner_score = competition.get_or_create_score(winner)
        loser_score = competition.get_or_create_score(loser)

        winner_new_score, loser_new_score = rate_1vs1(
            Rating(winner_score.score, winner_score.stdev),
            Rating(loser_score.score, loser_score.stdev)
        )

        winner_score.score = winner_new_score.mu
        winner_score.stdev = winner_new_score.sigma
        winner_score.save()

        loser_score.score = loser_new_score.mu
        loser_score.stdev = loser_new_score.sigma
        loser_score.save()

        HistoricalScore.objects.create(
            game=self,
            score=winner_score.score,
            stdev=winner_score.stdev,
            player=winner,
        )

        HistoricalScore.objects.create(
            game=self,
            score=loser_score.score,
            stdev=loser_score.stdev,
            player=loser,
        )

        if notify:
            new_rankings = competition.get_ranking_by_player()

            for player in [winner, loser]:
                if (player not in old_rankings or
                        old_rankings[player] != new_rankings[player]):
                    signals.ranking_changed.send(
                        sender=self,
                        player=player,
                        old_ranking=(old_rankings[player]
                                     if player in old_rankings else None),
                        new_ranking=new_rankings[player],
                        competition=competition
                    )

    def get_opponent(self, player):
        """
        Return the opponent player relative to the given player.
        """
        return self.winner if self.winner_id != player.id else self.loser
