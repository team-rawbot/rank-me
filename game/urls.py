from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns(
    '',
    url(r'^game/new/$', views.add, name='game_add'),
    url(r'^game/(?P<game_id>\d+)/$', views.detail, name='game_detail'),
    url(r'^team/(?P<team_id>\d+)/$', views.team, name='team_detail'),
    url(r'^competition/new/$', views.create_competition,
        name='competition_add'),
    url(r'^competition/(?P<slug>[\w-]+)/$', views.view_competition,
        name='competition_detail'),
)
