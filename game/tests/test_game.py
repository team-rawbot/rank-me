from django.test import TestCase

from ..factories import UserFactory
from ..models import Game


class TestGameAnnouncement(TestCase):
    @classmethod
    def setUp(self):
        # Create 4 dummy users
        self.users = [UserFactory() for id in range(4)]

    def test_game_announcement(self):
        Game.objects.announce(self.users[0], self.users[1])
        game = Game.objects.get()
        self.assertEquals(game.winner.users.get(), self.users[0])
        self.assertEquals(game.loser.users.get(), self.users[1])
        self.assertLess(game.loser.score, game.winner.score)
