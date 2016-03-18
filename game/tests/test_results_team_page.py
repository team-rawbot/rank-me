from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from game.models import Competition, Game
from rankme.tests import RankMeTestCase

from .factories import UserFactory, CompetitionFactory

User = get_user_model()


class TestResultsPlayerPage(RankMeTestCase):
    def setUp(self):
        super(TestResultsPlayerPage, self).setUp()

        # Create one competition and one user.
        # Then add this user to the competition
        self.default_competition = CompetitionFactory()
        self.user = UserFactory()
        self.default_competition.players.add(self.user)

    def login(self):
        self.client.login(username=self.user.username, password='password')

    def test_page_unavailability(self):
        self.login()

        response = self.client.get(reverse('player_detail', kwargs={
            'player_id': 1,
            'competition_slug': self.default_competition.slug
        }))
        self.assertEqual(404, response.status_code)

    def test_page_availability(self):
        sylvain = UserFactory()
        christoph = UserFactory()

        game = Game.objects.announce(
            sylvain, christoph, self.default_competition
        )

        self.login()
        response = self.client.get(reverse('player_detail', kwargs={
            'player_id': game.winner_id,
            'competition_slug': self.default_competition.slug
        }))
        self.assertEqual(200, response.status_code)

    def test_page_results(self):
        sylvain = UserFactory()
        christoph = UserFactory()

        Game.objects.announce(sylvain, christoph, self.default_competition)
        Game.objects.announce(sylvain, christoph, self.default_competition)
        game = Game.objects.announce(
            christoph, sylvain, self.default_competition
        )

        christoph_id = game.winner_id
        sylvain_id = game.loser_id

        self.login()
        response = self.client.get(reverse('player_detail', kwargs={
            'player_id': sylvain_id,
            'competition_slug': self.default_competition.slug
        }))

        self.assertContains(response, '<table class="team-statistics')
        self.assertContains(response, '<table id="head-2-head-results"')
        self.assertContains(response, '<th>Longest Winning Streak</th>')
        self.assertEqual(response.context['longest_streak'], 2)

        response = self.client.get(reverse('player_detail', kwargs={
            'player_id': christoph_id,
            'competition_slug': self.default_competition.slug
        }))

        self.assertContains(response, '<table class="team-statistics')
        self.assertContains(response, '<table id="head-2-head-results"')
        self.assertContains(response, '<th>Longest Winning Streak</th>')
        self.assertEqual(response.context['longest_streak'], 1)
