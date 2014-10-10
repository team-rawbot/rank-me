# coding=UTF-8

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from game.models import Competition, Game

from rankme.utils import RankMeTestCase

from .factories import UserFactory, CompetitionFactory

User = get_user_model()


class TestResultsPage(RankMeTestCase):
    def setUp(self):
        super(TestResultsPage, self).setUp()
        self.default_competition = CompetitionFactory()

    def test_page_availability(self):
        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': self.default_competition.slug
        }))
        self.assertEqual(302, response.status_code)

    def test_page_without_results(self):
        john = UserFactory()

        self.default_competition.players.add(john)

        self.client.login(username=john.username, password='password')
        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': self.default_competition.slug
        }))

        self.assertContains(response, '<div class="scores"')
        self.assertContains(response, 'No scores registered yet')
        self.assertContains(response, '<div class="latest-results')
        self.assertContains(response, 'No result yet')

    """
    User accesses the results page only when logged
    """
    def test_login(self):
        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': self.default_competition.slug
        }))
        self.assertEqual(302, response.status_code)

        john = UserFactory()

        self.default_competition.players.add(john)

        self.client.login(username=john.username, password='password')
        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': self.default_competition.slug
        }))
        self.assertContains(response, '<div class="scores"')

    def test_page_with_results(self):
        # create 2 users (automatically creates corresponding teams)
        laurent = UserFactory()
        rolf = UserFactory()

        self.default_competition.players.add(laurent)
        self.default_competition.players.add(rolf)

        # create 1 game
        game = Game.objects.announce(laurent, rolf, self.default_competition)
        game.save()

        self.client.login(username=rolf.username, password='password')
        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': self.default_competition.slug
        }))

        self.assertContains(response, '<div class="scores"')
        self.assertNotContains(response, 'No scores registered yet')
        self.assertContains(response, '<div class="score-board')
        self.assertContains(response, '<tr class="score-item"', 2)
        self.assertContains(response, '<div class="latest-results')
        self.assertContains(response, '<table class="games')
        self.assertContains(response, '<tr class="game-item', 1)
