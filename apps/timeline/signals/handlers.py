from django.db.models.signals import post_delete
from django.dispatch import receiver

from ...game.signals import (
    competition_created, game_played, ranking_changed,
    user_joined_competition, user_left_competition
)
from ...game.models import Game
from ..models import Event


@receiver(competition_created)
def publish_competition_created(sender, **kwargs):
    event = Event(event_type=Event.TYPE_COMPETITION_CREATED,
                  details={
                      'competition': {
                          'id': sender.id,
                          'name': sender.name,
                          'slug': sender.slug
                      }
                  })
    event.save()


@receiver(user_joined_competition)
def publish_user_joined_competition(sender, user, **kwargs):
    event = Event(event_type=Event.TYPE_USER_JOINED_COMPETITION,
                  competition=sender,
                  details={
                      'user': {
                          'id': user.id,
                          'name': user.profile.get_full_name(),
                          'avatar': user.profile.avatar
                      }
                  })
    event.save()


@receiver(user_left_competition)
def publish_user_left_competition(sender, user, **kwargs):
    event = Event(event_type=Event.TYPE_USER_LEFT_COMPETITION,
                  competition=sender,
                  details={
                      'user': {
                          'id': user.id,
                          'name': user.profile.get_full_name(),
                          'avatar': user.profile.avatar
                      }
                  })
    event.save()


@receiver(game_played)
def publish_game_played(sender, **kwargs):
    players = []
    for player in (sender.winner, sender.loser):
        players.append({
            "id": player.id,
            "name": player.get_full_name(),
            "avatar": player.profile.avatar,
        })

    event = Event(event_type=Event.TYPE_GAME_PLAYED,
                  competition=sender.competition,
                  details={
                      "winner": players[0],
                      "loser": players[1],
                      "game_id": sender.id,
                  })
    event.save()


@receiver(post_delete, sender=Game)
def delete_related_events(sender, instance, **kwargs):
    Event.objects.filter(details__game_id=instance.id).delete()


@receiver(ranking_changed)
def publish_ranking_changed(sender, player, old_ranking, new_ranking,
                            competition, **kwargs):
    player_details = {
        "id": player.id,
        "name": player.get_full_name(),
        "avatar": player.profile.avatar,
    }

    event = Event(event_type=Event.TYPE_RANKING_CHANGED,
                  competition=competition, details={
                      "player": player_details,
                      "old_ranking": old_ranking,
                      "new_ranking": new_ranking,
                      "game_id": sender.id,
                  })
    event.save()
