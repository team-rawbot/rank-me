from django.dispatch import receiver

import mock

from rankme.tests import RankMeTestCase

from .factories import UserFactory, CompetitionFactory
from ..models import Game
from ..signals import ranking_changed


class TestTeamGetOrCreate(RankMeTestCase):
    def setUp(self):
        super(TestTeamGetOrCreate, self).setUp()

        # Create 4 dummy users
        self.users = [UserFactory() for id in range(4)]
        self.default_competition = CompetitionFactory()

    def test_longest_streak(self):
        christoph, laurent, rolf = (UserFactory() for i in range(3))

        game = Game.objects.announce(christoph, rolf, self.default_competition)
        self.assertEqual(
            self.default_competition.get_longest_streak(game.winner), 1
        )
        self.assertEqual(
            self.default_competition.get_longest_streak(game.loser), 0
        )
        game = Game.objects.announce(christoph, rolf, self.default_competition)
        self.assertEqual(
            self.default_competition.get_longest_streak(game.winner), 2
        )
        game = Game.objects.announce(christoph, laurent,
                                     self.default_competition)
        self.assertEqual(
            self.default_competition.get_longest_streak(game.winner), 3
        )

        # C-C-C-Combo breaker
        game = Game.objects.announce(rolf, christoph, self.default_competition)
        self.assertEqual(
            self.default_competition.get_longest_streak(game.loser), 3
        )
        self.assertEqual(
            self.default_competition.get_longest_streak(game.winner), 1
        )

        game = Game.objects.announce(christoph, rolf, self.default_competition)
        self.assertEqual(
            self.default_competition.get_longest_streak(game.winner), 3
        )
        Game.objects.announce(christoph, rolf, self.default_competition)
        Game.objects.announce(christoph, rolf, self.default_competition)
        game = Game.objects.announce(christoph, laurent,
                                     self.default_competition)
        self.assertEqual(
            self.default_competition.get_longest_streak(game.winner), 4
        )

    def test_head2head(self):
        christoph, laurent, rolf = (UserFactory() for i in range(3))
        for player in [christoph, laurent, rolf]:
            self.default_competition.add_user_access(player)

        game = Game.objects.announce(christoph, rolf, self.default_competition)
        winner_head2head = self.default_competition.get_head2head(game.winner)
        loser_head2head = self.default_competition.get_head2head(game.loser)

        self.assertNotIn(game.winner, winner_head2head)
        self.assertNotIn(game.loser, loser_head2head)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 0)
        self.assertEqual(len(winner_head2head[game.loser]['games']), 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 0)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)
        self.assertEqual(len(loser_head2head[game.winner]['games']), 1)

        game = Game.objects.announce(rolf, christoph, self.default_competition)
        winner_head2head = self.default_competition.get_head2head(game.winner)
        loser_head2head = self.default_competition.get_head2head(game.loser)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 1)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)

        game = Game.objects.announce(rolf, christoph, self.default_competition)
        winner_head2head = self.default_competition.get_head2head(game.winner)
        loser_head2head = self.default_competition.get_head2head(game.loser)

        self.assertEqual(winner_head2head[game.loser]['wins'], 2)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 1)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 2)

        game = Game.objects.announce(laurent, christoph,
                                     self.default_competition)
        winner_head2head = self.default_competition.get_head2head(game.winner)
        loser_head2head = self.default_competition.get_head2head(game.loser)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 0)

        self.assertEqual(loser_head2head[game.winner]['wins'], 0)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)

        # Since Laurent never played against rolf, it shouldn't be in the
        # head2head
        self.assertNotIn(rolf, winner_head2head)


class TestTeamSignals(RankMeTestCase):
    def setUp(self):
        super(TestTeamSignals, self).setUp()

        self.default_competition = CompetitionFactory()

    def test_ranking_changed_signal(self):
        ranking_changed_receiver = receiver(ranking_changed)(mock.Mock())

        christoph, laurent, rolf = (UserFactory() for i in range(3))

        game1 = Game.objects.announce(rolf, christoph,
                                      self.default_competition)
        game2 = Game.objects.announce(christoph, rolf,
                                      self.default_competition)
        Game.objects.announce(christoph, rolf, self.default_competition)

        self.assertEqual(ranking_changed_receiver.call_count, 4)
        args_list = ranking_changed_receiver.call_args_list

        self.assertEqual(
            args_list, [
                mock.call(player=rolf, old_ranking=None, sender=game1,
                          new_ranking=1, signal=mock.ANY,
                          competition=self.default_competition),
                mock.call(player=christoph, old_ranking=None, sender=game1,
                          new_ranking=2, signal=mock.ANY,
                          competition=self.default_competition),
                mock.call(player=christoph, old_ranking=2, sender=game2,
                          new_ranking=1, signal=mock.ANY,
                          competition=self.default_competition),
                mock.call(player=rolf, old_ranking=1, sender=game2,
                          new_ranking=2, signal=mock.ANY,
                          competition=self.default_competition),
            ]
        )
