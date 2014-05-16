from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import UserFactory

User = get_user_model()


class TestAddResultPage(TestCase):
    def test_form_validation(self):
        # create 2 users
        laurent = UserFactory()
        rolf = UserFactory()

        # Unauthenticated users should be redirected to the login form to add a
        # result
        response = self.client.get(reverse('game_add'))
        self.assertEqual(302, response.status_code)

        self.client.login(username=laurent.username, password='password')
        response = self.client.get(reverse('game_add'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<form id="add-result')

        # test form validation

        # no user is specified
        response = self.client.post(reverse('game_add'), {})
        self.assertFormError(response, 'form', 'loser', 'This field is required.')
        self.assertFormError(response, 'form', 'winner', 'This field is required.')

        # only winner is specified
        response = self.client.post(reverse('game_add'), {'winner': laurent.id})
        self.assertFormError(response, 'form', 'loser', 'This field is required.')

        # winner and loser are the same user
        response = self.client.post(reverse('game_add'), {'winner': laurent.id, 'loser': laurent.id})
        self.assertFormError(response, 'form', None, 'Winner and loser can\'t be the same player!')

        # no error should be redirected to results page
        response = self.client.post(reverse('game_add'), {'winner': laurent.id, 'loser': rolf.id}, follow=True)
        self.assertRedirects(response, '/', 302, 200)
