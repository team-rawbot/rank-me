from django.conf import settings
from django.db import models

from trueskill import Rating, rate_1vs1


class Score(models.Model):
    competition = models.ForeignKey('Competition', related_name='scores')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='scores')
    score = models.FloatField('skills', default=settings.GAME_INITIAL_MU)
    stdev = models.FloatField('standard deviation',
                              default=settings.GAME_INITIAL_SIGMA)

    class Meta:
        unique_together = (
            ('competition', 'player'),
        )

    def __str__(self):
        return '[%s] %s: mu = %s, s = %s' % (self.competition.name,
                                             self.player.get_full_name(),
                                             self.score, self.stdev)


class HistoricalScoreManager(models.Manager):
    def get_latest(self, nb_games, competition):
        return (self.get_queryset()
                .select_related('game', 'game__winner', 'game__loser')
                .filter(game__competition=competition)
                .order_by('-id')[:nb_games])

    def get_default(self):
        return HistoricalScore(
            score=settings.GAME_INITIAL_MU,
            stdev=settings.GAME_INITIAL_SIGMA,
        )


class HistoricalScore(models.Model):
    game = models.ForeignKey('Game', related_name='historical_scores')
    player = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='historical_scores')
    score = models.FloatField('Current player score')
    stdev = models.FloatField('Current player standard deviation',
                              default=settings.GAME_INITIAL_SIGMA)

    objects = HistoricalScoreManager()

    class Meta:
        unique_together = (
            ('player', 'game'),
        )


def update_players_scores(winner, loser, game):
    """
    Compute the new score of the winner and the loser, update their scores and
    create ``HistoricalScore`` objects.
    """
    winner_score = game.competition.get_or_create_score(winner)
    loser_score = game.competition.get_or_create_score(loser)

    winner_new_score, loser_new_score = rate_1vs1(
        Rating(winner_score.score, winner_score.stdev),
        Rating(loser_score.score, loser_score.stdev)
    )

    update_player_score(winner_score, winner_new_score, game)
    update_player_score(loser_score, loser_new_score, game)


def update_player_score(old_score, new_score, game):
    """
    Update the player score with the new TrueSkill score. The ``game``
    parameter is used to track the game the update is coming from to create the
    ``HistoricalScore`` object.
    """
    old_score.score = new_score.mu
    old_score.stdev = new_score.sigma
    old_score.save()

    HistoricalScore.objects.create(
        game=game,
        score=old_score.score,
        stdev=old_score.stdev,
        player=old_score.player,
    )
