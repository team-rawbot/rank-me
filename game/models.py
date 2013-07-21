from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from trueskill import Rating, rate_1vs1


class Game(models.Model):
    winner = models.ForeignKey(User, related_name='+')
    loser = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return '%s beats %s' % (
            self.winner,
            self.loser
        )

class Rank(models.Model):
    user = models.ForeignKey(User, related_name='+')
    rank = models.IntegerField(default=1000)

    def update_rank(self, winner_id, loser_id):
        winner_rank_object = Rank.objects.get(id=winner_id)
        loser_rank_object = Rank.objects.get(id=loser_id)
        winner_new_rating, loser_new_rating = rate_1vs1(Rating(winner_rank_object.rank), Rating(loser_rank_object))

        winner_rank_object.rank = winner_new_rating
        winner_rank_object.save()
        loser_rank_object.rank = loser_new_rating
        loser_rank_object.save()

    def get_score_board(self):
        # todo
        pass

    def __str__(self):
        return '%s (%d)' % (
            self.user.username,
            self.rank
        )
