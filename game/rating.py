import abc
from trueskill import Rating, rate_1vs1, quality_1vs1


class _AbstractRating(object):
    __metaclass__ = abc.ABCMeta

    def rate(self, winner, loser):
        return self._rate(winner, loser)

    def quality(self, a, b):
        return self._quality(a, b)

    @abc.abstractmethod
    def _rate(self, winner, loser):
        return

    @abc.abstractmethod
    def _quality(self, a, b):
        return


class _TrueSkill(_AbstractRating):
    def _rating(self, score):
        return Rating(score.score, score.stdev)

    def _rate(self, winner, loser):
        return rate_1vs1(
            self._rating(winner),
            self._rating(loser)
        )

    def _quality(self, a, b):
        return quality_1vs1(
            self._rating(a),
            self._rating(b)
        )


rating = _TrueSkill()
