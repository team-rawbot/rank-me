from django.test import TestCase

from .factories import UserFactory
from ..models import Team


class TestTeamGetOrCreate(TestCase):
    @classmethod
    def setUp(self):
        # Create 4 dummy users
        self.users = [UserFactory(id=id) for id in range(4)]

    def test_team_creation(self):
        team, created = Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 1)

        team, created = Team.objects.get_or_create_from_players(
            self.users[0].id
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 2)

        team, created = Team.objects.get_or_create_from_players(
            self.users[1].id
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 3)

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
        self.assertItemsEqual(team.users.all(), self.users[0:2])

        # Check that team (0, 1) is equal to team (0, 1)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertFalse(created)
        self.assertEqual(Team.objects.count(), 1)

        # Check that team (1, 0) is equal to team (0, 1)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[1].id, self.users[0].id)
        )
        self.assertFalse(created)
        self.assertEqual(Team.objects.count(), 1)

        # Check that team (1, 2) is different from team (0, 1)
        team, created = Team.objects.get_or_create_from_players(
            (self.users[1].id, self.users[2].id)
        )
        self.assertTrue(created)
        self.assertEqual(Team.objects.count(), 2)
