from django.dispatch import receiver
from django.test import TestCase

import mock

from .factories import UserFactory
from ..models import Competition, Game, Team
from ..signals import team_ranking_changed


class TestTeamGetOrCreate(TestCase):
    @classmethod
    def setUp(self):
        # Create 4 dummy users
        self.users = [UserFactory() for id in range(4)]
        self.default_competition = Competition.objects.get_default_competition()

    def assertUsersEqual(self, first, second):
        def users_to_id_list(users):
            return sorted([user.id for user in users])

        first_ids = users_to_id_list(first)
        second_ids = users_to_id_list(second)

        return len(first_ids) == len(second_ids) and first_ids == second_ids

    def test_team_creation(self):
        team, created = Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 1)
        self.assertUsersEqual(team.users.all(), self.users[0:2])

        team, created = Team.objects.get_or_create_from_players(
            self.users[0].id
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 2)
        self.assertUsersEqual(team.users.all(), [self.users[0]])

        team, created = Team.objects.get_or_create_from_players(
            self.users[1].id
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 3)
        self.assertUsersEqual(team.users.all(), [self.users[1]])

    def test_team_uniqueness(self):
        """
        Test that calling get_or_create_from_players on the same set of players
        creates the team and then just returns it.
        """
        team, created = Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 1)
        self.assertUsersEqual(team.users.all(), self.users[0:2])

        # Check that team (0, 1) is equal to team (0, 1)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertFalse(created)
        self.assertEqual(Team.objects.count(), 1)
        self.assertUsersEqual(team.users.all(), self.users[0:2])

        # Check that team (1, 0) is equal to team (0, 1)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[1].id, self.users[0].id)
        )
        self.assertFalse(created)
        self.assertEqual(Team.objects.count(), 1)
        self.assertUsersEqual(team.users.all(), self.users[0:2])

        # Check that team (1, 2) is different from team (0, 1)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[1].id, self.users[2].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 2)
        self.assertUsersEqual(team.users.all(), self.users[1:3])

    def test_team_overlap(self):
        """
        Test that an overlapping team (eg. (0, 1, 2) vs (0, 1)) is reported as
        a new team.
        """
        team, created = Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 1)
        self.assertUsersEqual(team.users.all(), self.users[0:2])

        # Check that team (0, 1, 2) is different from (0, 1)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id, self.users[2].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 2)
        self.assertUsersEqual(team.users.all(), self.users[0:3])

        # Check that team (1, 2) is different from (0, 1, 2)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[1].id, self.users[2].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 3)
        self.assertUsersEqual(team.users.all(), self.users[1:3])

    def test_longest_streak(self):
        christoph, laurent, rolf = (UserFactory() for i in range(3))

        game = Game.objects.announce(christoph, rolf, self.default_competition)
        self.assertEqual(
            game.winner.get_longest_streak(self.default_competition), 1
        )
        self.assertEqual(
            game.loser.get_longest_streak(self.default_competition), 0
        )
        game = Game.objects.announce(christoph, rolf, self.default_competition)
        self.assertEqual(
            game.winner.get_longest_streak(self.default_competition), 2
        )
        game = Game.objects.announce(christoph, laurent,
                                     self.default_competition)
        self.assertEqual(
            game.winner.get_longest_streak(self.default_competition), 3
        )

        # C-C-C-Combo breaker
        game = Game.objects.announce(rolf, christoph, self.default_competition)
        self.assertEqual(
            game.loser.get_longest_streak(self.default_competition), 3
        )
        self.assertEqual(
            game.winner.get_longest_streak(self.default_competition), 1
        )

        game = Game.objects.announce(christoph, rolf, self.default_competition)
        self.assertEqual(
            game.winner.get_longest_streak(self.default_competition), 3
        )
        Game.objects.announce(christoph, rolf, self.default_competition)
        Game.objects.announce(christoph, rolf, self.default_competition)
        game = Game.objects.announce(christoph, laurent,
                                     self.default_competition)
        self.assertEqual(
            game.winner.get_longest_streak(self.default_competition), 4
        )

    def test_head2head(self):
        christoph, laurent, rolf = (UserFactory() for i in range(3))

        game = Game.objects.announce(christoph, rolf, self.default_competition)
        winner_head2head = game.winner.get_head2head(self.default_competition)
        loser_head2head = game.loser.get_head2head(self.default_competition)

        self.assertNotIn(game.winner, winner_head2head)
        self.assertNotIn(game.loser, loser_head2head)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 0)
        self.assertEqual(len(winner_head2head[game.loser]['games']), 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 0)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)
        self.assertEqual(len(loser_head2head[game.winner]['games']), 1)

        game = Game.objects.announce(rolf, christoph, self.default_competition)
        winner_head2head = game.winner.get_head2head(self.default_competition)
        loser_head2head = game.loser.get_head2head(self.default_competition)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 1)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)

        game = Game.objects.announce(rolf, christoph, self.default_competition)
        winner_head2head = game.winner.get_head2head(self.default_competition)
        loser_head2head = game.loser.get_head2head(self.default_competition)

        self.assertEqual(winner_head2head[game.loser]['wins'], 2)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 1)

        self.assertEqual(loser_head2head[game.winner]['wins'], 1)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 2)

        game = Game.objects.announce(laurent, christoph,
                                     self.default_competition)
        winner_head2head = game.winner.get_head2head(self.default_competition)
        loser_head2head = game.loser.get_head2head(self.default_competition)

        self.assertEqual(winner_head2head[game.loser]['wins'], 1)
        self.assertEqual(winner_head2head[game.loser]['defeats'], 0)

        self.assertEqual(loser_head2head[game.winner]['wins'], 0)
        self.assertEqual(loser_head2head[game.winner]['defeats'], 1)

        # Since Laurent never played against rolf, it shouldn't be in the
        # head2head
        self.assertNotIn(rolf.teams.first(), winner_head2head)

    def test_team_ranking_changed_signal(self):
        team_ranking_changed_receiver = receiver(
            team_ranking_changed
        )(mock.Mock())

        christoph, laurent, rolf = (UserFactory() for i in range(3))

        game1 = Game.objects.announce(rolf, christoph,
                                      self.default_competition)
        game2 = Game.objects.announce(christoph, rolf,
                                      self.default_competition)
        Game.objects.announce(christoph, rolf, self.default_competition)

        self.assertEqual(team_ranking_changed_receiver.call_count, 4)
        args_list = team_ranking_changed_receiver.call_args_list

        rolf_team = rolf.teams.get()
        christoph_team = christoph.teams.get()

        self.assertEqual(
            args_list, [
                mock.call(team=rolf_team, old_ranking=None, sender=game1,
                          new_ranking=1, signal=mock.ANY),
                mock.call(team=christoph_team, old_ranking=None, sender=game1,
                          new_ranking=2, signal=mock.ANY),
                mock.call(team=christoph_team, old_ranking=2, sender=game2,
                          new_ranking=1, signal=mock.ANY),
                mock.call(team=rolf_team, old_ranking=1, sender=game2,
                          new_ranking=2, signal=mock.ANY),
            ]
        )
