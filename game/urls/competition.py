from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url(r'^$', 'competition_detail', name='competition_detail'),
    url(r'^scores$', 'competition_detail_score_chart', name='competition_detail_score_chart'),
    url(r'^game/new/$', 'game_add', name='game_add'),
    url(r'^game/remove/(?P<game_id>\d+)$', 'game_remove', name='game_remove'),
    url(r'^team/(?P<team_id>\d+)/$', 'team_detail', name='team_detail'),
)
