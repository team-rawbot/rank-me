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
        self.assertContains(response, '<li class="score-item">laurent (1028)</li>')
        self.assertContains(response, '<li class="score-item">rolf (971)</li>')

        # create a 2nd game (as usual Laurent wins)
        game = Game.objects.announce(winner=laurent, loser=rolf)
        game.save()

        response = client.get('/results/')
        self.assertContains(response, '<li class="score-item">laurent (1036)</li>')
        self.assertContains(response, '<li class="score-item">rolf (962)</li>')
