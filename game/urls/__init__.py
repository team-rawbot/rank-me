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
    url(r'^clubs/$', 'club_list_all', name='club_list_all'),
    url(r'^clubs/new/$', 'club_add', name='club_add'),
    url(r'^clubs/(?P<club_slug>[\w-]+)/edit/', 'club_edit', name='club_edit'),
    url(r'^clubs/(?P<club_slug>[\w-]+)/', 'club_detail', name='club_detail'),
)
