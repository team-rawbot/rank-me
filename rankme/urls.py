from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views

import social.apps.django_app.urls

from timeline import views as timeline_views
from game import urls as game_urls
from api import urls as api_urls
from user import urls as user_urls

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', timeline_views.index, name='homepage'),
    url(r'', include(game_urls)),
    url(r'', include(api_urls)),
    url(r'^profile/', include(user_urls)),
    url('', include(social.apps.django_app.urls, namespace='social')),
    url(r'^logout/$', django.contrib.auth.views.logout, {
        'next_page': '/'
        }, name='auth_logout')
]
