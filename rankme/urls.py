from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from game import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rankme.views.home', name='home'),
    # url(r'^rankme/', include('rankme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', views.index, name='homepage'),
    url(r'^results/', include('game.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^competition/$', views.create_competition, name='create_competition'),
    url(r'^comp/(?P<id>\d+)$', views.view_competition, name='view_competition'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
        'next_page': '/'
        }, name='auth_logout')
)
