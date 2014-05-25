from django.dispatch import Signal


game_played = Signal()
team_ranking_changed = Signal(providing_args=[
    'team', 'old_ranking', 'new_ranking', 'competition'
])
