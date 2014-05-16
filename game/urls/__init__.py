from django.conf.urls import patterns, include, url

from game import views

urlpatterns = patterns(
    '',
    url(r'^team/(?P<team_id>\d+)/$', views.team, name='team_detail'),
    url(r'^competition/new/$', views.create_competition,
        name='competition_add'),
    url(r'^competition/(?P<competition_slug>[\w-]+)/', include('game.urls.competition'))
)
