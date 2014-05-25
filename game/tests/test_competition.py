import datetime
import pytz

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

from rankme.utils import RankMeTestCase

from ..models import Competition
from .factories import UserFactory


class TestCompetition(RankMeTestCase):
    def setUp(self):
        super(TestCompetition, self).setUp()

        self.user = UserFactory()
        self.client.login(username=self.user.username, password='password')

    def test_create_competition(self):
        response = self.client.get(reverse('competition_add'))
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse('competition_add'), {})
        self.assertContains(response, "This field is required.")

        response = self.client.post(reverse('competition_add'), {
            'name': 'ATP Tournament 2014',
            'description': 'Official ATP tournament',
            'start_date': '2014-05-03 00:00:00',
            'end_date': '2014-06-03 00:00:00'
        })
        self.assertRedirects(response, reverse('competition_detail', kwargs={
            'competition_slug': 'atp-tournament-2014'
        }))
        self.assertEqual(Competition.objects.all().count(), 2)
        competition = Competition.objects.get(slug='atp-tournament-2014')
        self.assertEqual(competition.name, 'ATP Tournament 2014')
        self.assertEqual(competition.description, 'Official ATP tournament')
        self.assertEqual(
            competition.start_date,
            timezone.make_aware(
                datetime.datetime(2014, 5, 3, 0, 0, 0),
                pytz.timezone(settings.TIME_ZONE)
            )
        )
