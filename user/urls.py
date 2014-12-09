from django.conf.urls import patterns, url

urlpatterns = patterns(
    'user.views',
    url(r'^$', 'index', name='profile'),
    url(r'^edit/$', 'edit', name='edit_profile'),
    url(r'^(?P<user_id>\d+)/$', 'index', name='profile'),
)
