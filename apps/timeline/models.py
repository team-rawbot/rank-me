from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _


class EventManager(models.Manager):
    def get_all_for_player(self, player):
        return self.select_related('competition').filter(
            Q(competition__in=player.competitions.all()) | Q(competition=None)
        )


class Event(models.Model):
    TYPE_RANKING_CHANGED = 'ranking_changed'
    TYPE_GAME_PLAYED = 'game_played'
    TYPE_COMPETITION_CREATED = 'competition_created'
    TYPE_USER_JOINED_COMPETITION = 'user_joined_competition'
    TYPE_USER_LEFT_COMPETITION = 'user_left_competition'
    TYPES = (
        (TYPE_GAME_PLAYED, _('Game played')),
        (TYPE_RANKING_CHANGED, _('Ranking changed')),
        (TYPE_COMPETITION_CREATED, _('Competition created')),
        (TYPE_USER_JOINED_COMPETITION, _('User joined competition')),
        (TYPE_USER_LEFT_COMPETITION, _('User left competition')),
    )

    event_type = models.CharField(max_length=50, choices=TYPES)
    details = JSONField(default=dict)
    date = models.DateTimeField(auto_now_add=True)
    competition = models.ForeignKey('game.Competition', null=True)

    objects = EventManager()

    class Meta:
        ordering = ["-date"]

    def get_details(self):
        return self.details
