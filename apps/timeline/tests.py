from rankme.tests import RankMeTestCase
from ..game.tests.factories import CompetitionFactory, UserFactory

from .models import Event


class TimelineTestCase(RankMeTestCase):
    def test_delete_game_deletes_related_events(self):
        players = [UserFactory() for _ in range(2)]
        competition = CompetitionFactory()
        events_before_game = Event.objects.count()
        game = competition.add_game(players[0], players[1])
        game.delete()
        self.assertEqual(Event.objects.count(), events_before_game)
