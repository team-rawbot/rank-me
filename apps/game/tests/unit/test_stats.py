from freezegun import freeze_time

from rankme.tests import RankMeTestCase

from ... import stats
from ..factories import CompetitionFactory, UserFactory


class StatsTestCase(RankMeTestCase):
    def test_get_stats_per_week_limits_to_given_number_of_days(self):
        users = [UserFactory() for _ in range(2)]

        with freeze_time('2016-03-22'):
            # Create the competition in the freeze_time block so the start date
            # is right, otherwise we'd have to set it manually... BORING
            competition = CompetitionFactory()
            competition.add_game(users[0], users[1])

        with freeze_time('2016-03-28'):
            competition.add_game(users[0], users[1])

        with freeze_time('2016-04-04'):
            self.assertEqual(len(stats.get_stats_per_week(users[0], 7)), 1)

    def test_get_stats_per_week_rounds_to_monday(self):
        users = [UserFactory() for _ in range(2)]

        # That's monday
        with freeze_time('2016-03-22'):
            # Create the competition in the freeze_time block so the start date
            # is right, otherwise we'd have to set it manually... BORING
            competition = CompetitionFactory()
            competition.add_game(users[0], users[1])

        # That's monday
        with freeze_time('2016-03-28'):
            self.assertEqual(len(stats.get_stats_per_week(users[0], 3)), 1)
