from django.core.urlresolvers import reverse

from rankme.tests import RankMeTestCase

from .factories import UserFactory, CompetitionFactory


class TestAddResultPage(RankMeTestCase):
    def test_form_validation(self):
        competition = CompetitionFactory()
        game_add_url = reverse('game_add', kwargs={
            'competition_slug': competition.slug
        })

        # create 2 users and add them into the competition
        laurent = UserFactory()
        rolf = UserFactory()

        competition.players.add(laurent)
        competition.players.add(rolf)

        # Unauthenticated users should be redirected to the login form to add a
        # result
        response = self.client.get(game_add_url)
        self.assertEqual(302, response.status_code)

        self.client.login(username=laurent.username, password='password')
        response = self.client.get(game_add_url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<form id="add-result')

        # test form validation

        # no user is specified
        response = self.client.post(game_add_url, {})
        self.assertFormError(response, 'form', 'loser', 'This field is required.')
        self.assertFormError(response, 'form', 'winner', 'This field is required.')

        # only winner is specified
        response = self.client.post(game_add_url, {'winner': laurent.id})
        self.assertFormError(response, 'form', 'loser', 'This field is required.')

        # winner and loser are the same user
        response = self.client.post(game_add_url, {'winner': laurent.id, 'loser': laurent.id})
        self.assertFormError(response, 'form', None, 'Winner and loser can\'t be the same player!')

        # no error should be redirected to results page
        response = self.client.post(game_add_url, {'winner': laurent.id, 'loser': rolf.id}, follow=True)
        self.assertRedirects(response, reverse('competition_detail', kwargs={
            'competition_slug': competition.slug
        }), 302, 200)
