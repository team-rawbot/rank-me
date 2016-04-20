from django.contrib import admin

from .models import Competition, Game, Score, Sport


class CompetitionAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'start_date', 'end_date', 'slug',
              'players', 'creator']


class ScoreAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(ScoreAdmin, self).get_queryset(request)

        return queryset.select_related('competition')

admin.site.register(Game)
admin.site.register(Sport)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Competition, CompetitionAdmin)
