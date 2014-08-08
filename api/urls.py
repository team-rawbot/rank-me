from django.conf.urls import patterns, url, include
from rest_framework import routers

from .views import competition_view_set

router = routers.DefaultRouter()
router.register(r'competitions', competition_view_set)

urlpatterns = patterns(
    'api.views',
    url(r'^api/', include([
        url(
            r'^register-by-token/(?P<backend>[^/]+)/$',
            'api.views.register_by_access_token',
            name='register_by_access_token',
        ),
        url(r'^', include(router.urls)),
        url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
        ])),
)
