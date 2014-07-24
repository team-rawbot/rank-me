from django.contrib import admin
from game.models import Competition, Game, Score, Team


class CompetitionAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'start_date', 'end_date', 'slug']

admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Score)
admin.site.register(Competition, CompetitionAdmin)
