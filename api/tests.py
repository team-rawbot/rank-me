from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CompetitionTests(APITestCase):
    def test_list_competitions(self):
        """
        Ensure we can list all competitions.
        """
        url = reverse('competition-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
