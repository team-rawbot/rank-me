from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'game.views',
    url(r'^team/(?P<team_id>\d+)/$', 'team_detail', name='team_detail'),
    url(r'^competition/new/$', 'competition_add',
        name='competition_add'),
    url(r'^competition/(?P<competition_slug>[\w-]+)/',
        include('game.urls.competition'))
)
