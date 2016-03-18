from django.conf.urls import include, url

from . import views

competition_patterns = [
    url(r'^$', views.competition_detail, name='competition_detail'),
    url(r'^edit/$', views.competition_edit, name='competition_edit'),
    url(r'^scores/$', views.competition_detail_score_chart, name='competition_detail_score_chart'),
    url(r'^scores/(?P<start>\d+)$', views.competition_detail_score_chart, name='competition_detail_score_chart_with_start'),
    url(r'^game/new/$', views.game_add, name='game_add'),
    url(r'^game/remove/$', views.game_remove, name='game_remove'),
    url(r'^player/(?P<player_id>\d+)/$', views.player_detail, name='player_detail'),
    url(r'^join/$', views.competition_join, name='competition_join'),
    url(r'^leave/$', views.competition_leave, name='competition_leave'),
]

urlpatterns = [
    url(r'^competitions/$', views.competition_list_all,
        name='competition_list_all'),
    url(r'^competitions/new/$', views.competition_add,
        name='competition_add'),
    url(r'^competitions/(?P<competition_slug>[\w-]+)/',
        include(competition_patterns)),
    url(r'^player/(?P<player_id>\d+)/$', views.player_general_detail,
        name='player_general_detail'),
]
