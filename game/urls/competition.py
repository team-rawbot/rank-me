from django.conf.urls import patterns, url

from .. import views

urlpatterns = patterns(
    '',
    url(r'^$', views.view_competition, name='competition_detail'),
    url(r'^game/new/$', views.add, name='game_add'),
    url(r'^game/(?P<game_id>\d+)/$', views.detail, name='game_detail'),
)
