from django.conf import settings
from django.db import models


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
    competition = models.ForeignKey('Competition', related_name='historical_scores')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='historical_scores')
    score = models.FloatField('Current player score')
    stdev = models.FloatField('Current player standard deviation',
                              default=settings.GAME_INITIAL_SIGMA)

    objects = HistoricalScoreManager()

    class Meta:
        unique_together = (
            ('player', 'game', 'competition'),
        )
