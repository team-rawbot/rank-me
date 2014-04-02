# coding=UTF-8

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from game.models import Game

User = get_user_model()

class TestResultsPage(TestCase):
    def test_page_availability(self):
        client = self.client
        response = client.get('/results/')
        self.assertEqual(200, response.status_code)

    def test_page_without_results(self):
        rolf = User.objects.create_user('rolf', 'rolf@test.com', 'pass')
        rolf.save()

        client = self.client
        client.login(username='rolf', password='pass')
        response = client.get('/results/')
        self.assertContains(response, '<div class="scores"')
        self.assertContains(response, 'No scores registered yet')
        self.assertNotContains(response, '<ul class="score-board"')
        self.assertContains(response, '<div class="latest-results"')
        self.assertContains(response, 'No result yet')

    """
    User accesses the results page only when logged
    """
    def test_login(self):
        client = self.client
        response = client.get('/results/')
        self.assertNotContains(response, '<div class="scores"')

        rolf = User.objects.create_user('rolf', 'rolf@test.com', 'pass')
        rolf.save()
        client.login(username='rolf', password='pass')
        response = client.get('/results/')
        self.assertContains(response, '<div class="scores"')

    def test_page_with_results(self):
        # create 2 users (automatically creates corresponding teams)
        laurent = User.objects.create_user('laurent', 'laurent@test.com', 'pass')
        laurent.save()

        rolf = User.objects.create_user('rolf', 'rolf@test.com', 'pass')
        rolf.save()

        # create 1 game
        game = Game.objects.announce(winner=laurent, loser=rolf)
        game.save()

        client = self.client

        client.login(username='rolf', password='pass')
        response = client.get('/results/')

        self.assertContains(response, '<div class="scores"')
        self.assertNotContains(response, 'No scores registered yet')
        self.assertContains(response, '<ol class="score-board"')
        self.assertContains(response, '<li class="score-item"', 2)
        self.assertContains(response, '<div class="latest-results"')
        self.assertContains(response, '<ul class="games')
        self.assertContains(response, '<li class="game-item', 1)

        # specifically test ranking
        self.assertContains(response, '<li class="score-item" title="W: 1, L: 0')
        self.assertContains(response, '<li class="score-item" title="W: 0, L: 1')

        # create a 2nd game (as sometimes Laurent wins)
        game = Game.objects.announce(winner=laurent, loser=rolf)

        response = client.get('/results/')
        self.assertContains(response, '<li class="score-item" title="W: 2, L: 0')
        self.assertContains(response, '<li class="score-item" title="W: 0, L: 2')
