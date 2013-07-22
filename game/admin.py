from django.contrib import admin
from game.models import Game, Rank


class GameAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        Rank.update_rank(obj.winner.id, obj.loser.id)
        obj.save()

admin.site.register(Game, GameAdmin)


class RankAdmin(admin.ModelAdmin):
    pass

admin.site.register(Rank, RankAdmin)
