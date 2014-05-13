from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='game_index'),
    url(r'^add/$', views.add, name='game_add'),
    url(r'^(?P<game_id>\d+)/$', views.detail, name='game_detail'),
    url(r'^team/(?P<team_id>\d+)/$', views.team, name='team_detail'),
)
