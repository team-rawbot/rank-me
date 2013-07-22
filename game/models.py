from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from trueskill import Rating, rate_1vs1


class Game(models.Model):
    winner = models.ForeignKey(User, related_name='+')
    loser = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(default=datetime.now)

    @classmethod
    def get_latest_results(cls):
        return cls.objects.all().order_by('-date')[:20]

    def __str__(self):
        return '%s beats %s' % (
            self.winner,
            self.loser
        )


class Rank(models.Model):
    user = models.ForeignKey(User, related_name='+')
    rank = models.IntegerField(default=1000)
    stdev = models.FloatField('standard deviation')

    @classmethod
    def update_rank(cls, winner_id, loser_id):
        winner_rank_object = cls.objects.get(id=winner_id)
        loser_rank_object = cls.objects.get(id=loser_id)
        winner_new_rating, loser_new_rating = rate_1vs1(
            Rating(winner_rank_object.rank, winner_rank_object.stdev),
            Rating(loser_rank_object.rank, loser_rank_object.stdev)
        )

        winner_rank_object.rank = winner_new_rating.mu
        winner_rank_object.stdev = winner_new_rating.sigma
        winner_rank_object.save()
        loser_rank_object.rank = loser_new_rating.mu
        loser_rank_object.stdev = loser_new_rating.sigma
        loser_rank_object.save()

    @classmethod
    def get_score_board(cls):
        return cls.objects.all().order_by('-rank')

    def __str__(self):
        return '%s (%d/%d)' % (
            self.user.username,
            self.rank,
            self.stdev
        )
