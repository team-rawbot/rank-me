from datetime import timedelta

import mock

from django.dispatch import receiver
from django.utils import timezone

from rankme.tests import RankMeTestCase

from ...exceptions import CannotLeaveCompetitionError
from ...models import Competition, Game
from ...signals import competition_created
from ..factories import CompetitionFactory, UserFactory


class CompetitionTestCase(RankMeTestCase):
    def test_get_visible_doesnt_return_non_visible_competition(self):
        c1, c2 = CompetitionFactory(), CompetitionFactory()
        user = UserFactory()

        c1.add_user_access(user)
        self.assertNotIn(c2, Competition.objects.get_visible_for_user(user))

    def test_get_visible_returns_visible_competitions(self):
        c1 = CompetitionFactory()
        CompetitionFactory()
        user = UserFactory()

        c1.add_user_access(user)
        self.assertIn(c1, Competition.objects.get_visible_for_user(user))

    def test_save_competition_generates_slug(self):
        c = Competition.objects.create(name='Hello World',
                                       creator=UserFactory())
        self.assertEqual(c.slug, 'hello-world')

    def test_save_new_competition_sends_created_signal(self):
        competition_created_receiver = receiver(
            competition_created
        )(mock.Mock())
        competition = CompetitionFactory()

        competition_created_receiver.assert_called_once_with(
            sender=competition, signal=mock.ANY
        )

    def test_save_existing_competition_doesnt_send_created_signal(self):
        competition = CompetitionFactory()

        competition_created_receiver = receiver(
            competition_created
        )(mock.Mock())
        competition.name = 'Foobar'
        competition.save()

        competition_created_receiver.assert_not_called()

    def test_add_game_creates_game(self):
        c = CompetitionFactory()
        winner, loser = UserFactory(), UserFactory()
        c.add_game(winner, loser)
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.get()
        self.assertEqual(game.competition, c)
        self.assertEqual(game.winner, winner)
        self.assertEqual(game.loser, loser)

    def test_get_games_played_by_only_returns_played_games(self):
        c = CompetitionFactory()
        users = [UserFactory() for _ in range(0, 3)]
        played_game = c.add_game(users[0], users[1])
        c.add_game(users[1], users[2])
        games = c.get_games_played_by(users[0])
        self.assertEqual(list(games), [played_game])

    def test_ongoing_competition_manager_doesnt_return_past_competition(self):
        c = CompetitionFactory(end_date=timezone.now() - timedelta(days=1))
        self.assertNotIn(c, Competition.ongoing_objects.all())

    def test_ongoing_competition_manager_doesnt_return_future_competition(self):
        c = CompetitionFactory(start_date=timezone.now() + timedelta(days=1))
        self.assertNotIn(c, Competition.ongoing_objects.all())

    def test_ongoing_competition_manager_returns_competition_with_empty_end_date(self):
        c = CompetitionFactory(
            end_date=None,
            start_date=timezone.now() - timedelta(days=1)
        )
        self.assertIn(c, Competition.ongoing_objects.all())

    def test_ongoing_competition_manager_returns_started_and_unfinished_competition(self):
        c = CompetitionFactory(
            end_date=timezone.now() + timedelta(days=1),
            start_date=timezone.now() - timedelta(days=1)
        )
        self.assertIn(c, Competition.ongoing_objects.all())

    def test_creator_cannot_leave_competition(self):
        user = UserFactory()
        competition = CompetitionFactory(creator=user)
        with self.assertRaises(CannotLeaveCompetitionError):
            competition.remove_user_access(user)
