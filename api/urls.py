from django.conf.urls import patterns, url, include
from rest_framework import routers

from .views import CompetitionViewSet

router = routers.DefaultRouter()
router.register(r'competitions', CompetitionViewSet)

urlpatterns = patterns(
    'api.views',
    url(r'^api/', include([
        url(r'^', include(router.urls)),
        url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
        ])),
)
