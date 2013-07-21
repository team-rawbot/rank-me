from django.contrib import admin
from game.models import Game, Rank


class GameAdmin(admin.ModelAdmin):
    pass

admin.site.register(Game, GameAdmin)


class RankAdmin(admin.ModelAdmin):
    pass

admin.site.register(Rank, RankAdmin)
