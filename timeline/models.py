import json

from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django_hstore import hstore

from game.signals import (
    competition_created, game_played, team_ranking_changed,
    user_joined_competition
)
from rankme.utils import memoize


@receiver(competition_created)
def publish_competition_created(sender, **kwargs):
    event = Event(event_type=Event.TYPE_COMPETITION_CREATED,
                  details={
                      'competition': {
                          'id': sender.id,
                          'name': sender.name,
                          'slug': sender.slug
                      }
                  })
    event.save()


@receiver(user_joined_competition)
def publish_user_joined_competition(sender, user, **kwargs):
    event = Event(event_type=Event.TYPE_USER_JOINED_COMPETITION,
                  competition=sender,
                  details={
                      'user': {
                          'id': user.id,
                          'name': user.get_profile().get_full_name(),
                          'avatar': user.get_profile().avatar
                      }
                  })
    event.save()


@receiver(game_played)
def publish_game_played(sender, **kwargs):
    teams = []
    for team in (sender.winner, sender.loser):
        teams.append({
            "id": team.id,
            "name": team.get_name(),
            "avatar": team.users.first().get_profile().avatar,
        })

    event = Event(event_type=Event.TYPE_GAME_PLAYED,
                  competition=sender.competitions.first(),
                  details={"winner": teams[0], "loser": teams[1]})
    event.save()


@receiver(team_ranking_changed)
def publish_team_ranking_changed(sender, team, old_ranking, new_ranking,
                                 competition, **kwargs):
    player = {
        "id": team.id,
        "name": team.get_name(),
        "avatar": team.users.first().get_profile().avatar,
    }

    event = Event(event_type=Event.TYPE_RANKING_CHANGED,
                  competition=competition, details={
                      "player": player,
                      "old_ranking": old_ranking,
                      "new_ranking": new_ranking
                  })
    event.save()


class EventManager(hstore.HStoreManager):
    def get_all_for_user(self, user):
        return self.filter(
            Q(competition__in=user.competitions.all()) | Q(competition=None)
        )


class Event(models.Model):
    TYPE_RANKING_CHANGED = 'ranking_changed'
    TYPE_GAME_PLAYED = 'game_played'
    TYPE_COMPETITION_CREATED = 'competition_created'
    TYPE_USER_JOINED_COMPETITION = 'user_joined_competition'
    TYPES = (
        (TYPE_GAME_PLAYED, _('Game played')),
        (TYPE_RANKING_CHANGED, _('Ranking changed')),
        (TYPE_COMPETITION_CREATED, _('Competition created')),
        (TYPE_USER_JOINED_COMPETITION, _('User joined competition')),
    )

    event_type = models.CharField(max_length=50, choices=TYPES)
    details = hstore.DictionaryField()
    date = models.DateTimeField(auto_now_add=True)
    competition = models.ForeignKey('game.Competition', null=True)

    objects = EventManager()

    class Meta:
        ordering = ["-date"]

    @memoize
    def get_details(self):
        details = {}

        for key, value in self.details.iteritems():
            try:
                details[key] = json.loads(value)
            except:
                details[key] = value

        return details
