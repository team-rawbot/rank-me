import slack

from game.models import Competition, Game
from game.tests.factories import UserFactory
from rankme.utils import RankMeTestCase


class SlackTest(RankMeTestCase):
    def test_message_sending(self):
        users = [UserFactory() for id in range(2)]
        default_competition = Competition.objects.get_default_competition()

        Game.objects.announce(users[0], users[1],
                              default_competition)

        # 3 messages should have been posted: the game result announcement, the
        # position change of the winner and the position change of the loser
        self.assertEqual(
            slack.Slacker.return_value.chat.post_message.call_count,
            3
        )
