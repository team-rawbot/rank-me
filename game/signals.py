from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from trueskill import Rating, rate_1vs1

from .models import Game, Team


@receiver(post_save, sender=Game)
def update_score(sender, **kwargs):
    if not kwargs['created']:
        return

    game = kwargs['instance']

    winner = game.winner
    loser = game.loser
    winner_new_score, loser_new_score = rate_1vs1(
        Rating(winner.score, winner.stdev),
        Rating(loser.score, loser.stdev)
    )

    winner.score = winner_new_score.mu
    winner.stdev = winner_new_score.sigma
    winner.save()
    loser.score = loser_new_score.mu
    loser.stdev = loser_new_score.sigma
    loser.save()


@receiver(post_save, sender=User)
def create_user_team(sender, **kwargs):
    """
    Automatically create a team when a user is created
    """
    if not kwargs['created']:
        return

    team = Team()
    team.save()
    team.users.add(kwargs['instance'])
