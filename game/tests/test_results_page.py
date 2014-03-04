# coding=UTF-8

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from game.models import Game

User = get_user_model()


class TestResultsPage(TestCase):
    def test_page_availability(self):
        client = Client()
        response = client.get('/results/')
        self.assertEqual(200, response.status_code)

    def test_page_without_results(self):
        client = Client()
        response = client.get('/results/')
        self.assertContains(response, '<div class="scores"')
        self.assertContains(response, 'No scores registered yet')
        self.assertNotContains(response, '<ul class="score-board"')
        self.assertContains(response, '<div class="latest-results"')
        self.assertContains(response, 'No result yet')

    def test_page_with_results(self):
        # create 2 users (automatically creates corresponding teams)
        laurent = User.objects.create_user('laurent', 'laurent@test.com', 'pass')
        laurent.save()

        rolf = User.objects.create_user('rolf', 'rolf@test.com', 'pass')
        rolf.save()

        # create 1 game
        game = Game.objects.announce(winner=laurent, loser=rolf)
        game.save()

        client = Client()
        response = client.get('/results/')

        self.assertContains(response, '<div class="scores"')
        self.assertNotContains(response, 'No scores registered yet')
        self.assertContains(response, '<ol class="score-board"')
        self.assertContains(response, '<li class="score-item"', 2)
        self.assertContains(response, '<div class="latest-results"')
        self.assertContains(response, '<ul class="games')
        self.assertContains(response, '<li class="game-item', 1)


        # specifically test ranking
        self.assertContains(response, '<li class="score-item" title="W: 1, L: 0, σ: 7.16880"><strong>laurent</strong> (29.4)</li>')
        self.assertContains(response, '<li class="score-item" title="W: 0, L: 1, σ: 7.16880"><strong>rolf</strong> (20.6)</li>')

        # create a 2nd game (as usual Laurent wins)
        game = Game.objects.announce(winner=laurent, loser=rolf)
        game.save()

        response = client.get('/results/')
        self.assertContains(response, '<li class="score-item" title="W: 2, L: 0, σ: 6.52104"><strong>laurent</strong> (31.2)</li>')
        self.assertContains(response, '<li class="score-item" title="W: 0, L: 2, σ: 6.52104"><strong>rolf</strong> (18.8)</li>')
