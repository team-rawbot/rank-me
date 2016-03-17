from django.conf.urls import url, include
from rest_framework import routers, urls as rest_framework_urls
from .views import (
    CompetitionViewSet, TeamViewSet, UserViewSet, GameViewSet, ScoreViewSet,
    register_by_access_token
)

router = routers.DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)
router.register(r'scores', ScoreViewSet)

urlpatterns = [
    url(r'^api/', include([
        url(
            r'^register-by-token/(?P<backend>[^/]+)/$',
            register_by_access_token, name='register_by_access_token',
            ),
        url(r'^', include(router.urls)),
        url(r'^api-auth/', include(rest_framework_urls, namespace='rest_framework'))
        ])),
]
