from django.dispatch import receiver
from game.signals import game_played

from django.db import models
from django_hstore import hstore
from game.models import Competition

import json

@receiver(game_played)
def publish_game_played(sender, **kwargs):
    winner = {
        "id": sender.winner.id,
        "name": sender.winner.get_name(),
        "avatar": sender.winner.users.first().get_profile().avatar,
    }
    loser = {
        "id": sender.loser.id,
        "name": sender.loser.get_name(),
        "avatar": sender.loser.users.first().get_profile().avatar
    }
    event = Event(event_type="game", competition=sender.competitions.first(),
        details={"winner": winner, "loser": loser}
    )
    event.save()

class Event(models.Model):
    # TODO ENUM
    event_type = models.CharField(max_length=50)
    details = hstore.DictionaryField()
    date = models.DateTimeField(auto_now_add=True)
    competition = models.ForeignKey(Competition)

    objects = hstore.HStoreManager()

    def get_winner(self):
        return json.loads(self.details["winner"])

    def get_loser(self):
        return json.loads(self.details["loser"])

    class Meta:
        ordering = ["-date"]
