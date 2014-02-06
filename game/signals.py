from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Game


@receiver(post_save, sender=Game)
def update_score(sender, **kwargs):
    if not kwargs['created']:
        return

    game = kwargs['instance']
    game.update_score()
