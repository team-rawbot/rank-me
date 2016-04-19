from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.dispatch import receiver
from django.utils import timezone

import mock

from rankme.tests import RankMeTestCase

from ..factories import UserFactory, CompetitionFactory
from ...models import Game, HistoricalScore
from ...signals import game_played


class GameTestCase(RankMeTestCase):
    def setUp(self):
        super().setUp()

        # Create 4 dummy users
        self.users = [UserFactory() for id in range(4)]
        self.default_competition = CompetitionFactory()

    def test_game_announcement(self):
        Game.objects.announce(self.users[0], self.users[1],
                              self.default_competition)
        game = Game.objects.get()
        self.assertEqual(game.winner, self.users[0])
        self.assertEqual(game.loser, self.users[1])
        self.assertLess(game.loser.scores.get().score,
                        game.winner.scores.get().score)

    def test_game_date(self):
        game1 = Game.objects.announce(self.users[0], self.users[1],
                                      self.default_competition)
        game2 = Game.objects.announce(self.users[1], self.users[0],
                                      self.default_competition)
        self.assertGreater(game2.date, game1.date)

    def test_game_announcement_signal(self):
        game_played_receiver = receiver(game_played)(mock.Mock())

        game = Game.objects.announce(self.users[0], self.users[1],
                                     self.default_competition)
        game_played_receiver.assert_called_once_with(
            sender=game, signal=mock.ANY
        )

        # Check that the 'game played' signal is fired only when the game
        # object is created, not modified
        game_played_receiver = receiver(game_played)(mock.Mock())

        game.date = timezone.now()
        game.save()

        self.assertEqual(game_played_receiver.call_count, 0)

    def test_same_winner_loser_raises_validation_error(self):
        game = Game()
        game.winner = self.users[0]
        game.loser = self.users[0]
        self.assertRaises(ValidationError, game.full_clean)

    def test_game_deletion_removes_associated_scores(self):
        game = self.default_competition.add_game(self.users[0], self.users[1])
        game.delete()
        self.assertEqual(HistoricalScore.objects.count(), 0)

    def test_single_game_for_player_deletion_removes_score(self):
        game = self.default_competition.add_game(self.users[0], self.users[1])
        game.delete()
        with self.assertRaises(ObjectDoesNotExist):
            self.default_competition.get_score(self.users[0])

    def test_multiple_games_for_player_deletion_doesnt_remove_score(self):
        self.default_competition.add_game(self.users[0], self.users[1])
        game = self.default_competition.add_game(self.users[0], self.users[1])
        game.delete()
        self.assertTrue(self.default_competition.get_score(self.users[0]))

    def test_game_deletion_resets_score(self):
        game = self.default_competition.add_game(self.users[0], self.users[1])
        historical_score = game.historical_scores.get(player=self.users[0])
        game = self.default_competition.add_game(self.users[0], self.users[1])
        game.delete()
        score = self.default_competition.get_score(self.users[0])
        self.assertEqual(
            (score.score, score.stdev),
            (historical_score.score, historical_score.stdev)
        )

    def test_game_announcement_creates_historical_scores(self):
        self.default_competition.add_game(self.users[0], self.users[1])
        self.assertEqual(HistoricalScore.objects.count(), 2)
        self.default_competition.add_game(self.users[0], self.users[1])
        self.assertEqual(HistoricalScore.objects.count(), 4)

    def test_game_announcement_updates_scores(self):
        self.default_competition.add_game(self.users[0], self.users[1])
        old_score = self.default_competition.get_score(self.users[0])
        self.default_competition.add_game(self.users[0], self.users[1])
        new_score = self.default_competition.get_score(self.users[0])
        self.assertTrue(new_score.score > old_score.score)

    def test_get_opponent_returns_opponent(self):
        game = self.default_competition.add_game(self.users[0], self.users[1])
        self.assertEqual(game.get_opponent(self.users[0]), self.users[1])
