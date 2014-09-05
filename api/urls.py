from django.conf.urls import patterns, url, include
from rest_framework import routers

from .views import CompetitionViewSet, TeamViewSet

router = routers.DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = patterns(
    'api.views',
    url(r'^api/', include([
        url(
            r'^register-by-token/(?P<backend>[^/]+)/$',
            'api.views.register_by_access_token',
            name='register_by_access_token',
        ),
        url(r'^', include(router.urls)),
        url(r'^results/add/$', 'api.views.add_result', name='api_add_result'),
        url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
        ])),
)
