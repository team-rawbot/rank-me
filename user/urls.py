from django.conf.urls import patterns, url

urlpatterns = patterns(
    'user.views',
    url(r'^$', 'index', name='profile'),
    url(r'^edit$', 'edit', name='edit_profile'),
)
