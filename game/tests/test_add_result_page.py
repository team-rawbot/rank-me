from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import UserFactory
from ..models import Competition

User = get_user_model()


class TestAddResultPage(TestCase):
    def test_form_validation(self):
        competition = Competition.objects.get_default_competition()
        game_add_url = reverse('game_add', kwargs={
            'competition_slug': competition.slug
        })

        # create 2 users
        laurent = UserFactory()
        rolf = UserFactory()

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
