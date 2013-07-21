from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<game_id>\d+)/$', views.detail, name='detail'),
)