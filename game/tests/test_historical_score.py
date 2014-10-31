import json

from rankme.utils import RankMeTestCase

from .factories import UserFactory, CompetitionFactory
from ..models import HistoricalScore, Game


class TestHistoricalScore(RankMeTestCase):
    def test_historical_score(self):
        users = [UserFactory() for _ in range(3)]
        default_competition = CompetitionFactory()

        HistoricalScore.clear()

        game = Game.objects.announce(users[0], users[1], default_competition)
        historical_scores = HistoricalScore.get_latest_results_by_team(default_competition)

        print historical_scores
        historical_scores = json.loads(historical_scores)['games']
        print historical_scores

        self.assertEqual(len(historical_scores), 1)
        self.assertEqual(historical_scores['winner']['game_id'], game.pk)
        self.assertEqual(historical_scores['winner']['position'], 1)
        self.assertEqual(historical_scores['loser']['position'], 2)
        self.assertNotIn(users[2], historical_scores)

        Game.objects.announce(users[1], users[0], default_competition)
        game = Game.objects.announce(users[1], users[0], default_competition)
        historical_scores = HistoricalScore.get_latest_results_by_team(default_competition)
        self.assertEqual(len(historical_scores), 2)

        self.assertEqual(historical_scores[game.winner][0]['position'], 2)
        self.assertEqual(historical_scores[game.loser][0]['position'], 1)
        self.assertEqual(historical_scores[game.winner][1]['position'], 1)
        self.assertEqual(historical_scores[game.loser][1]['position'], 2)
        self.assertEqual(historical_scores[game.winner][2]['position'], 1)
        self.assertEqual(historical_scores[game.loser][2]['position'], 2)

        historical_scores = HistoricalScore.get_latest_results_by_team(default_competition)
        self.assertEqual(len(historical_scores[game.winner]), 2)
