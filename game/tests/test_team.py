from django.test import TestCase

from .factories import UserFactory
from ..models import Team


class TestTeamGetOrCreate(TestCase):
    @classmethod
    def setUp(self):
        # Create 4 dummy users
        self.users = [UserFactory() for id in range(4)]

    def test_team_creation(self):
        self.assertEqual(Team.objects.count(), 0)
        Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertEqual(Team.objects.count(), 1)

        Team.objects.get_or_create_from_players(self.users[0].id)
        self.assertEqual(Team.objects.count(), 2)

        Team.objects.get_or_create_from_players(self.users[1].id)
        self.assertEqual(Team.objects.count(), 3)

    def test_team_uniqueness(self):
        """
        Test that calling get_or_create_from_players on the same set of players
        creates the team and then just returns it.
        """
        self.assertEqual(Team.objects.count(), 0)
        Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertEqual(Team.objects.count(), 1)

        Team.objects.get_or_create_from_players(
            (self.users[0].id, self.users[1].id)
        )
        self.assertEqual(Team.objects.count(), 1)

        Team.objects.get_or_create_from_players(
            (self.users[1].id, self.users[0].id)
        )
        self.assertEqual(Team.objects.count(), 1)

        Team.objects.get_or_create_from_players(
            (self.users[1].id, self.users[2].id)
        )
        self.assertEqual(Team.objects.count(), 2)
