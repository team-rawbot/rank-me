from django.dispatch import receiver
from django.utils import timezone

import mock

from rankme.tests import RankMeTestCase

from .factories import UserFactory, CompetitionFactory
from ..models import Game
from ..signals import game_played


class TestGameAnnouncement(RankMeTestCase):
    def setUp(self):
        super(TestGameAnnouncement, self).setUp()

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
