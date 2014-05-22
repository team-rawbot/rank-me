from six import StringIO

from django.core.management import call_command
from django.test import TestCase
from trueskill import Rating, rate_1vs1

from ..models import Competition, Game
from .factories import UserFactory


class RecalculateCommandTestCase(TestCase):
    def test_recalculate(self):
        """
        Test the recalculate command.
        """
        users = [UserFactory(), UserFactory()]
        default_competition = Competition.objects.get_default_competition()

        Game.objects.announce(users[0], users[1], default_competition)
        Game.objects.announce(users[0], users[1], default_competition)

        args = [25, 8]
        opts = {}
        stdout = StringIO()
        call_command('recalculate', stdout=stdout, *args, **opts)

        winner_score, loser_score = rate_1vs1(
            Rating(25, 8), Rating(25, 8)
        )
        expected_winner_score, expected_loser_score = rate_1vs1(
            Rating(winner_score.mu, winner_score.sigma),
            Rating(loser_score.mu, loser_score.sigma)
        )

        game = Game.objects.last()
        winner_score = game.winner.scores.get()
        loser_score = game.loser.scores.get()

        self.assertAlmostEqual(winner_score.score, expected_winner_score.mu)
        self.assertAlmostEqual(winner_score.stdev, expected_winner_score.sigma)
        self.assertAlmostEqual(loser_score.score, expected_loser_score.mu)
        self.assertAlmostEqual(loser_score.stdev, expected_loser_score.sigma)
