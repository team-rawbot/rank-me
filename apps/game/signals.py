from django.dispatch import Signal


competition_created = Signal()
user_joined_competition = Signal(providing_args=['user'])
user_left_competition = Signal(providing_args=['user'])
game_played = Signal()
ranking_changed = Signal(providing_args=[
    'player', 'old_ranking', 'new_ranking', 'competition'
])
