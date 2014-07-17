from django.contrib import admin
from game.models import Competition, Game, Score, Team


admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Score)
admin.site.register(Competition)
