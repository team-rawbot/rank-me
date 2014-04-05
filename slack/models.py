from django.dispatch import receiver
from game.signals import game_played, team_ranking_changed

from . import post_message


@receiver(game_played)
def publish_game_played(sender, **kwargs):
    post_message(u"%s wins against %s" % (
        sender.winner.get_name(),
        sender.loser.get_name()
    ))


@receiver(team_ranking_changed)
def publish_team_ranking_changed(sender, team, old_ranking, new_ranking, **kwargs):
    post_message(u"%s goes from #%s to #%s" % (
        team.get_name(),
        old_ranking,
        new_ranking
    ))
