from django.dispatch import receiver
from game.signals import game_played, team_ranking_changed

from . import post_message


@receiver(game_played)
def publish_game_played(sender, **kwargs):
    post_message(u"[{competitions}] {winner} wins against {loser}".format(
        competitions=' '.join(
            [competition.name for competition in sender.competitions.all()]
        ),
        winner=sender.winner.get_name(),
        loser=sender.loser.get_name()
    ))


@receiver(team_ranking_changed)
def publish_team_ranking_changed(sender, team, old_ranking, new_ranking,
                                 competition, **kwargs):
    if old_ranking is None:
        post_message(
            u"[{competition}] {player} enters the ranking and is"
            " #{ranking}".format(
                competition=competition,
                player=team.get_name(),
                ranking=new_ranking
            )
        )
    else:
        post_message(
            u"[{competition}] {player} goes from #{old_ranking} to"
            " #{new_ranking}".format(
                competition=competition,
                player=team.get_name(),
                old_ranking=old_ranking,
                new_ranking=new_ranking
            )
        )
