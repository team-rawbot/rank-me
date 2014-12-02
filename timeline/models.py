import json

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django_hstore import hstore

from game.signals import game_played, team_ranking_changed
from rankme.utils import memoize


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
        return self.filter(competition__in=user.competitions.all())


class Event(models.Model):
    TYPE_RANKING_CHANGED = 'ranking-changed'
    TYPE_GAME_PLAYED = 'game'
    TYPES = (
        (TYPE_GAME_PLAYED, _('Game played')),
        (TYPE_RANKING_CHANGED, _('Ranking changed')),
    )

    event_type = models.CharField(max_length=50, choices=TYPES)
    details = hstore.DictionaryField()
    date = models.DateTimeField(auto_now_add=True)
    competition = models.ForeignKey('game.Competition')

    objects = EventManager()

    class Meta:
        ordering = ["-date"]

    @memoize
    def get_details(self):
        details = {}
        try:
            for key in self.details:
                details[key] = json.loads(self.details[key])
        except:
            details[key] = self.details[key]

        return details
