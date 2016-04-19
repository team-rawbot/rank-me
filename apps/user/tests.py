from django.core.urlresolvers import reverse

from rankme.tests import RankMeTestCase
from ..game.tests.factories import CompetitionFactory, UserFactory


class UserTestCase(RankMeTestCase):
    def test_user_profile_page_returns_200(self):
        user = UserFactory(password='foobar')
        self.client.login(username=user.username, password='foobar')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_page_with_scores_returns_200(self):
        user = UserFactory(password='foobar')
        self.client.login(username=user.username, password='foobar')

        opponent = UserFactory()
        competition = CompetitionFactory()
        competition.add_game(user, opponent)
        competition.add_game(user, opponent)
        competition.add_game(opponent, user)

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
