from django.dispatch import Signal


competition_created = Signal()
user_joined_competition = Signal(providing_args=['user'])
game_played = Signal()
team_ranking_changed = Signal(providing_args=[
    'team', 'old_ranking', 'new_ranking', 'competition'
])
