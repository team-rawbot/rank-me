import datetime
import pytz

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

from rankme.tests import RankMeTestCase

from .factories import UserFactory


class TestHomepage(RankMeTestCase):
    def setUp(self):
        super(TestHomepage, self).setUp()

        self.user = UserFactory()
        self.client.login(username=self.user.username, password='password')

    def test_redirect_to_all_competitions_page(self):
        """
        Redirect to 'all competitions' page as we don't have homepage yet
        """
        response = self.client.get(reverse('homepage'))
        self.assertContains(response, '<small>%s</small>' % self.user.username)
