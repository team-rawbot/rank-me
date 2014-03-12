from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from game.models import Game

from .factories import UserFactory

User = get_user_model()


class TestResultsTeamPage(TestCase):
    def test_page_unavailability(self):
        response = self.client.get(
            reverse('team_detail', kwargs={'team_id': 1})
        )
        self.assertEqual(404, response.status_code)

    def test_page_availability(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = UserFactory()
        christoph = UserFactory()

        # create 1 game
        game = Game.objects.announce(winner=sylvain, loser=christoph)

        response = self.client.get(
            reverse('team_detail', kwargs={'team_id': game.winner_id})
        )
        self.assertEqual(200, response.status_code)

    def test_page_results(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = UserFactory()
        christoph = UserFactory()

        # create 3 game
        Game.objects.announce(winner=sylvain, loser=christoph)
        Game.objects.announce(winner=sylvain, loser=christoph)
        game = Game.objects.announce(winner=christoph, loser=sylvain)

        christoph_team_id = game.winner_id
        sylvain_team_id = game.loser_id

        response = self.client.get(
            reverse('team_detail', kwargs={'team_id': sylvain_team_id})
        )

        self.assertContains(response, '<ul class="team-statistics"')
        self.assertContains(response, '<ul class="head2head">')
        self.assertContains(response, '<li><strong>Longest Winning Streak</strong>: 2</li>')

        response = self.client.get(
            reverse('team_detail', kwargs={'team_id': christoph_team_id})
        )

        self.assertContains(response, '<ul class="team-statistics"')
        self.assertContains(response, '<ul class="head2head">')
        self.assertContains(response, '<li><strong>Longest Winning Streak</strong>: 1</li>')
