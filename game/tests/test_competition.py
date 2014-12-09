import datetime
import pytz

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

from rankme.tests import RankMeTestCase

from ..models import Competition
from .factories import UserFactory, CompetitionFactory


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
            'players': [self.user.id],
            'start_date': '2014-05-03 00:00:00',
            'end_date': '2014-06-03 00:00:00'
        })
        self.assertRedirects(response, reverse('competition_detail', kwargs={
            'competition_slug': 'atp-tournament-2014'
        }))
        self.assertEqual(Competition.objects.all().count(), 1)
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

    def test_edit_competition(self):
        competition = CompetitionFactory()

        response = self.client.get(reverse('competition_edit', kwargs={
            'competition_slug': competition.slug
        }))
        self.assertEqual(403, response.status_code)

        john = UserFactory()
        competition.creator_id = john.id
        competition.save()

        self.client.login(username=john.username, password='password')

        response = self.client.get(reverse('competition_edit', kwargs={
            'competition_slug': competition.slug
        }))
        self.assertEqual(200, response.status_code)

    def test_access_on_competition(self):
        """
        John has no access to defaut_competition by default
        Then add John to default_competition
        """
        competition = CompetitionFactory()

        john = UserFactory()
        self.client.login(username=john.username, password='password')

        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': competition.slug
        }))
        self.assertContains(response, '<h1>Access denied</h1>')

        competition.players.add(john)

        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': competition.slug
        }))
        self.assertContains(response, "<h1>%s" % competition.name)
