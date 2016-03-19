from django.dispatch import receiver

import mock

from rankme.tests import RankMeTestCase

from .factories import UserFactory, CompetitionFactory
from .. import stats
from ..signals import ranking_changed


class TestTeamGetOrCreate(RankMeTestCase):
    def setUp(self):
        super(TestTeamGetOrCreate, self).setUp()

        # Create 4 dummy users
        self.users = [UserFactory() for id in range(4)]
        self.default_competition = CompetitionFactory()

    def test_longest_streak(self):
        christoph, laurent, rolf = (UserFactory() for i in range(3))

        game = self.default_competition.add_game(christoph, rolf)
        self.assertEqual(
            stats.get_longest_streak(game.winner, self.default_competition), 1
        )
        self.assertEqual(
            stats.get_longest_streak(game.loser, self.default_competition), 0
        )
        game = self.default_competition.add_game(christoph, rolf)
        self.assertEqual(
            stats.get_longest_streak(game.winner, self.default_competition), 2
        )
        game = self.default_competition.add_game(christoph, laurent)
        self.assertEqual(
            stats.get_longest_streak(game.winner, self.default_competition), 3
        )

        # C-C-C-Combo breaker
        game = self.default_competition.add_game(rolf, christoph)
        self.assertEqual(
            stats.get_longest_streak(game.loser, self.default_competition), 3
        )
        self.assertEqual(
            stats.get_longest_streak(game.winner, self.default_competition), 1
        )

        game = self.default_competition.add_game(christoph, rolf)
        self.assertEqual(
            stats.get_longest_streak(game.winner, self.default_competition), 3
        )
        self.default_competition.add_game(christoph, rolf)
        self.default_competition.add_game(christoph, rolf)
        game = self.default_competition.add_game(christoph, laurent)
        self.assertEqual(
            stats.get_longest_streak(game.winner, self.default_competition), 4
        )

    def test_head2head(self):
        christoph, laurent, rolf = (UserFactory() for i in range(3))
        for player in [christoph, laurent, rolf]:
            self.default_competition.add_user_access(player)

        game = self.default_competition.add_game(christoph, rolf)
        winner_head2head = stats.get_head2head(game.winner, self.default_competition)
        loser_head2head = stats.get_head2head(game.loser, self.default_competition)

        self.assertNotIn(game.winner, winner_head2head)
        self.assertNotIn(game.loser, loser_head2head)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 0)
        self.assertEqual(len(winner_head2head[game.loser]['games']), 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 0)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)
        self.assertEqual(len(loser_head2head[game.winner]['games']), 1)

        game = self.default_competition.add_game(rolf, christoph)
        winner_head2head = stats.get_head2head(game.winner, self.default_competition)
        loser_head2head = stats.get_head2head(game.loser, self.default_competition)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 1)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)

        game = self.default_competition.add_game(rolf, christoph)
        winner_head2head = stats.get_head2head(game.winner, self.default_competition)
        loser_head2head = stats.get_head2head(game.loser, self.default_competition)

        self.assertEqual(winner_head2head[game.loser]['wins'], 2)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 1)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 2)

        game = self.default_competition.add_game(laurent, christoph)
        winner_head2head = stats.get_head2head(game.winner, self.default_competition)
        loser_head2head = stats.get_head2head(game.loser, self.default_competition)

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

        game1 = self.default_competition.add_game(rolf, christoph)
        game2 = self.default_competition.add_game(christoph, rolf)
        self.default_competition.add_game(christoph, rolf)

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
