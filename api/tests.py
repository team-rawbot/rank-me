from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from game.tests.factories import UserFactory, CompetitionFactory, TeamFactory


def test_route(self, route):
    user = UserFactory()
    self.client.force_authenticate(user)

    url = reverse('competition-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIsNotNone(response.data)


class CompetitionListTests(APITestCase):
    def test_list_competitions(self):
        """
        Ensure we can list all competitions.
        """
        test_route(self, 'competition-list')


class PlayersListTests(APITestCase):
    def test_list_players(self):
        """
        Ensure we can list all players.
        """
        test_route(self, 'team-list')


class GameCreateTest(APITestCase):
    def test_create_game(self):
        user = UserFactory()
        self.client.force_authenticate(user)

        user_winner = UserFactory()
        user_loser = UserFactory()

        data = {
            'winner_id': TeamFactory(users=(user_winner,)).id,
            'loser_id': TeamFactory(users=(user_loser,)).id,
            'competition_id': CompetitionFactory().id
        }

        url = reverse('game-list')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)
