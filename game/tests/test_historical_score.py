from django.test import TestCase

from .factories import UserFactory
from ..models import HistoricalScore, Game


class TestHistoricalScore(TestCase):
    def test_historical_score(self):
        users = [UserFactory() for _ in range(3)]

        game = Game.objects.announce(users[0], users[1])
        self.assertEquals(HistoricalScore.objects.count(), 1)

        historical_scores = HistoricalScore.objects.get_latest_results_by_team(10)
        self.assertEquals(len(historical_scores), 2)
        self.assertEquals(historical_scores[game.winner][0]['position'], 1)
        self.assertEquals(historical_scores[game.loser][0]['position'], 2)
        self.assertNotIn(users[2], historical_scores)

        Game.objects.announce(users[1], users[0])
        game = Game.objects.announce(users[1], users[0])
        self.assertEquals(HistoricalScore.objects.count(), 3)

        historical_scores = HistoricalScore.objects.get_latest_results_by_team(10)
        self.assertEquals(len(historical_scores), 2)

        self.assertEquals(historical_scores[game.winner][0]['position'], 2)
        self.assertEquals(historical_scores[game.loser][0]['position'], 1)
        self.assertEquals(historical_scores[game.winner][1]['position'], 1)
        self.assertEquals(historical_scores[game.loser][1]['position'], 2)
        self.assertEquals(historical_scores[game.winner][2]['position'], 1)
        self.assertEquals(historical_scores[game.loser][2]['position'], 2)

        historical_scores = HistoricalScore.objects.get_latest_results_by_team(2)
        self.assertEquals(len(historical_scores[game.winner]), 2)
