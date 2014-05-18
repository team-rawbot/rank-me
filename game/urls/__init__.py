from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'game.views',
    url(r'^competition/new/$', 'competition_add',
        name='competition_add'),
    url(r'^competition/(?P<competition_slug>[\w-]+)/',
        include('game.urls.competition')),
    url(r'^team/(?P<team_id>\d+)/$', 'team_general_detail',
        name='team_general_detail'),
)
