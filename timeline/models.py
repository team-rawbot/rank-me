from django.dispatch import receiver
from game.signals import game_played

from django.db import models
from django_hstore import hstore
from game.models import Competition

@receiver(game_played)
def publish_game_played(sender, **kwargs):
    event = Event(event_type="game", competition=sender.competitions.first(),
        details={"winner": sender.winner.get_name(), "loser": sender.loser.get_name()}
    )
    event.save()

class Event(models.Model):
    # TODO ENUM
    event_type = models.CharField(max_length=50)
    details = hstore.DictionaryField()
    date = models.DateTimeField(auto_now_add=True)
    competition = models.ForeignKey(Competition)

    class Meta:
        ordering = ["-date"]