from rankme.tests import RankMeTestCase

from ..factories import UserFactory, CompetitionFactory
from ... import stats
from ...models import HistoricalScore, Game


class TestHistoricalScore(RankMeTestCase):
    def test_historical_score(self):
        users = [UserFactory() for _ in range(3)]
        default_competition = CompetitionFactory()

        game = Game.objects.announce(users[0], users[1], default_competition)
        self.assertEqual(HistoricalScore.objects.count(), 2)

        historical_scores = stats.get_latest_results_by_player(
            default_competition, 10
        )
        self.assertEqual(len(historical_scores), 2)
        self.assertEqual(historical_scores[game.winner][0]['position'], 1)
        self.assertEqual(historical_scores[game.loser][0]['position'], 2)
        self.assertNotIn(users[2], historical_scores)

        Game.objects.announce(users[1], users[0], default_competition)
        game = Game.objects.announce(users[1], users[0], default_competition)
        self.assertEqual(HistoricalScore.objects.count(), 6)

        historical_scores = stats.get_latest_results_by_player(
            default_competition, 10
        )
        self.assertEqual(len(historical_scores), 2)

        self.assertEqual(historical_scores[game.winner][0]['position'], 2)
        self.assertEqual(historical_scores[game.loser][0]['position'], 1)
        self.assertEqual(historical_scores[game.winner][1]['position'], 1)
        self.assertEqual(historical_scores[game.loser][1]['position'], 2)
        self.assertEqual(historical_scores[game.winner][2]['position'], 1)
        self.assertEqual(historical_scores[game.loser][2]['position'], 2)

        historical_scores = stats.get_latest_results_by_player(
            default_competition, 2
        )
        self.assertEqual(len(historical_scores[game.winner]), 2)
