from django.contrib import admin
from game.models import Competition, Competitor, Game, Score, Team


class CompetitorInline(admin.TabularInline):
    model = Competitor


class CompetitionAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'start_date', 'end_date', 'slug']

    inlines = [
        CompetitorInline
    ]


class ScoreAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(ScoreAdmin, self).get_queryset(request)

        return queryset.select_related('competition')

admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Competition, CompetitionAdmin)
