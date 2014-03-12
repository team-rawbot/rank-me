from django.contrib.auth import get_user_model
from django.test import TestCase

from game.models import Game

from .factories import UserFactory

User = get_user_model()


class TestResultsTeamPage(TestCase):
    def test_page_unavailability(self):
        response = self.client.get('/results/team/1/')
        self.assertEqual(404, response.status_code)

    def test_page_availability(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = UserFactory()
        christoph = UserFactory()

        # create 1 game
        Game.objects.announce(winner=sylvain, loser=christoph)

        response = self.client.get('/results/team/1/')
        self.assertEqual(200, response.status_code)

    def test_page_results(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = UserFactory()
        christoph = UserFactory()

        # create 3 game
        Game.objects.announce(winner=sylvain, loser=christoph)
        Game.objects.announce(winner=sylvain, loser=christoph)
        Game.objects.announce(winner=christoph, loser=sylvain)

        response = self.client.get('/results/team/1/')

        self.assertContains(response, '<ul class="team-statistics"')
        self.assertContains(response, '<ul class="head2head">')
        self.assertContains(response, '<li><strong>Longest Winning Streak</strong>: 2</li>')

        response = self.client.get('/results/team/2/')

        self.assertContains(response, '<ul class="team-statistics"')
        self.assertContains(response, '<ul class="head2head">')
        self.assertContains(response, '<li><strong>Longest Winning Streak</strong>: 1</li>')
