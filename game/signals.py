from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from trueskill import Rating, rate_1vs1

from .models import Game, Rank


@receiver(post_save, sender=Game)
def update_rank(sender, **kwargs):
    if not kwargs['created']:
        return

    game = kwargs['instance']

    winner_rank = Rank.objects.get(user=game.winner)
    loser_rank = Rank.objects.get(user=game.loser)
    winner_new_rating, loser_new_rating = rate_1vs1(
        Rating(winner_rank.rank, winner_rank.stdev),
        Rating(loser_rank.rank, loser_rank.stdev)
    )

    winner_rank.rank = winner_new_rating.mu
    winner_rank.stdev = winner_new_rating.sigma
    winner_rank.save()
    loser_rank.rank = loser_new_rating.mu
    loser_rank.stdev = loser_new_rating.sigma
    loser_rank.save()


@receiver(post_save, sender=User)
def create_user_rank(sender, **kwargs):
    if not kwargs['created']:
        return

    Rank.objects.create(user=kwargs['instance'])
