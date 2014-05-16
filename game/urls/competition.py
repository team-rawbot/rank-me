from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url(r'^$', 'competition_detail', name='competition_detail'),
    url(r'^game/new/$', 'game_add', name='game_add'),
    url(r'^game/(?P<game_id>\d+)/$', 'game_detail', name='game_detail'),
)
