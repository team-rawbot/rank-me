from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'game.views.index', name='homepage'),
    url(r'', include('game.urls')),
    url(r'', include('api.urls')),
    url(r'^profile/', include('user.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
        'next_page': '/'
        }, name='auth_logout')
)
