from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'game.views',
    url(r'^competitions/$', 'competition_list_all',
        name='competition_list_all'),
    url(r'^competitions/new/$', 'competition_add',
        name='competition_add'),
    url(r'^competitions/(?P<competition_slug>[\w-]+)/',
        include('game.urls.competition')),
    url(r'^team/(?P<team_id>\d+)/$', 'team_general_detail',
        name='team_general_detail'),
)
