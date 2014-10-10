from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from game.models import Competition, Game
from rankme.utils import RankMeTestCase

from .factories import UserFactory

User = get_user_model()


class TestResultsTeamPage(RankMeTestCase):
    def setUp(self):
        super(TestResultsTeamPage, self).setUp()

        # Create one competition and one user.
        # Then add this user to the competition
        self.default_competition = Competition.objects.get_default_competition()
        self.user = UserFactory()
        self.default_competition.players.add(self.user)

    def login(self):
        self.client.login(username=self.user.username, password='password')

    def test_page_unavailability(self):
        self.login()

        response = self.client.get(reverse('team_detail', kwargs={
            'team_id': 1,
            'competition_slug': self.default_competition.slug
        }))
        self.assertEqual(404, response.status_code)

    def test_page_availability(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = UserFactory()
        christoph = UserFactory()

        # create 1 game
        game = Game.objects.announce(
            sylvain, christoph, self.default_competition
        )

        self.login()
        response = self.client.get( reverse('team_detail', kwargs={
            'team_id': game.winner_id,
            'competition_slug': self.default_competition.slug
        }))
        self.assertEqual(200, response.status_code)

    def test_page_results(self):
        # create 1 user (automatically creates corresponding teams)
        sylvain = UserFactory()
        christoph = UserFactory()

        # create 3 game
        Game.objects.announce(sylvain, christoph, self.default_competition)
        Game.objects.announce(sylvain, christoph, self.default_competition)
        game = Game.objects.announce(
            christoph, sylvain, self.default_competition
        )

        christoph_team_id = game.winner_id
        sylvain_team_id = game.loser_id

        self.login()
        response = self.client.get(reverse('team_detail', kwargs={
            'team_id': sylvain_team_id,
            'competition_slug': self.default_competition.slug
        }))

        self.assertContains(response, '<table class="team-statistics')
        self.assertContains(response, '<table id="head-2-head-results"')
        self.assertContains(response, '<th>Longest Winning Streak</th>')
        self.assertEqual(response.context['longest_streak'], 2)

        response = self.client.get(reverse('team_detail', kwargs={
            'team_id': christoph_team_id,
            'competition_slug': self.default_competition.slug
        }))

        self.assertContains(response, '<table class="team-statistics')
        self.assertContains(response, '<table id="head-2-head-results"')
        self.assertContains(response, '<th>Longest Winning Streak</th>')
        self.assertEqual(response.context['longest_streak'], 1)
