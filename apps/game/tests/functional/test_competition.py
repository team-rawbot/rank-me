import datetime
import pytz

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

from bs4 import BeautifulSoup

from rankme.tests import RankMeTestCase

from ...models import Competition
from ..factories import CompetitionFactory, SportFactory, UserFactory


class TestCompetition(RankMeTestCase):
    def setUp(self):
        super(TestCompetition, self).setUp()

        self.user = UserFactory()
        self.client.login(username=self.user.username, password='password')

    def test_create_competition(self):
        sport = SportFactory()

        response = self.client.get(reverse('competition_add'))
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse('competition_add'), {})
        self.assertContains(response, "This field is required.")

        response = self.client.post(reverse('competition_add'), {
            'name': 'ATP Tournament 2014',
            'description': 'Official ATP tournament',
            'players': [self.user.id],
            'start_date': '2014-05-03T00:00:00',
            'end_date': '2014-06-03T00:00:00',
            'sport': sport.id
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

    def test_access_on_inaccessible_competition_doesnt_show_competition(self):
        competition = CompetitionFactory()
        john = UserFactory()
        self.client.login(username=john.username, password='password')

        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': competition.slug
        }))
        self.assertEqual(response.status_code, 403)

    def test_access_on_accessible_competition_shows_competition(self):
        competition = CompetitionFactory()
        john = UserFactory()
        self.client.login(username=john.username, password='password')
        competition.players.add(john)

        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': competition.slug
        }))
        self.assertEqual(response.status_code, 200)

    def test_add_result_button_is_disabled_on_ended_competition(self):
        john = UserFactory()
        competition = CompetitionFactory(
            end_date=timezone.now() - datetime.timedelta(days=2)
        )
        competition.players.add(john)
        self.client.login(username=john.username, password='password')
        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': competition.slug
        }))
        soup = BeautifulSoup(response.content)
        add_result_button = soup.select_one('a#add-result-button')
        self.assertIn('disabled', add_result_button.attrs)

    def test_add_result_on_ended_competition_shows_error(self):
        john, joe = [UserFactory() for _ in range(2)]
        competition = CompetitionFactory(
            end_date=timezone.now() - datetime.timedelta(days=2)
        )
        for player in (john, joe):
            competition.players.add(player)
        self.client.login(username=john.username, password='password')
        response = self.client.post(reverse('game_add', kwargs={
            'competition_slug': competition.slug
        }), data={
            'winner': john,
            'loser': joe,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None,
                             "Cannot add result on inactive competition")

    def test_creator_doesnt_see_leave_competition_button(self):
        user = UserFactory()
        competition = CompetitionFactory(creator=user)
        self.client.login(username=user.username, password='password')

        response = self.client.get(reverse('competition_detail', kwargs={
            'competition_slug': competition.slug
        }))
        self.assertNotContains(response, "Leave competition")
