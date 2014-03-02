# coding=UTF-8

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from game.models import Game

User = get_user_model()

class TestResultsTeamPage(TestCase):
    
    def test_page_unavailability(self):
        client = Client()
        response = client.get('/results/team/1/')
        self.assertEqual(404, response.status_code)

    def test_page_availability(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = User.objects.create_user('sylvain', 'sylvain@test.com', 'pass')
        sylvain.save()

        christoph = User.objects.create_user('christoph', 'christoph@test.com', 'pass')
        christoph.save()

        # create 1 game
        game = Game.objects.announce(winner=sylvain, loser=christoph)
        game.save()

        client = Client()
        response = client.get('/results/team/1/')
        self.assertEqual(200, response.status_code)

    def test_page_results(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = User.objects.create_user('sylvain', 'sylvain@test.com', 'pass')
        sylvain.save()

        christoph = User.objects.create_user('christoph', 'christoph@test.com', 'pass')
        christoph.save()

        # create 3 game
        game = Game.objects.announce(winner=sylvain, loser=christoph)
        game.save()

        game = Game.objects.announce(winner=sylvain, loser=christoph)
        game.save()

        game = Game.objects.announce(winner=christoph, loser=sylvain)
        game.save()

        client = Client()
        response = client.get('/results/team/1/')

        self.assertContains(response, '<ul class="team-statistics"')
        self.assertContains(response, '<ul class="head2head">')
        self.assertContains(response, '<li><strong>Longest Winning Streak</strong>: 2</li>')

        response = client.get('/results/team/2/')

        self.assertContains(response, '<ul class="team-statistics"')
        self.assertContains(response, '<ul class="head2head">')
        self.assertContains(response, '<li><strong>Longest Winning Streak</strong>: 1</li>')