from django.dispatch import receiver

from ..game.signals import game_played, ranking_changed
from . import post_message


@receiver(game_played)
def publish_game_played(sender, **kwargs):
    post_message(u"[{competition}] {winner} wins against {loser}".format(
        competition=sender.competition.name,
        winner=sender.winner.get_full_name(),
        loser=sender.loser.get_full_name()
    ))


@receiver(ranking_changed)
def publish_ranking_changed(sender, player, old_ranking, new_ranking,
                            competition, **kwargs):
    if old_ranking is None:
        post_message(
            u"[{competition}] {player} enters the ranking and is"
            " #{ranking}".format(
                competition=competition,
                player=player.get_full_name(),
                ranking=new_ranking
            )
        )
    else:
        post_message(
            u"[{competition}] {player} goes from #{old_ranking} to"
            " #{new_ranking}".format(
                competition=competition,
                player=player.get_full_name(),
                old_ranking=old_ranking,
                new_ranking=new_ranking
            )
        )
