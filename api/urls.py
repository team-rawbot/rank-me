from django.conf.urls import url, include
from rest_framework import routers
from api.views import CompetitionViewSet, TeamViewSet, UserViewSet, GameViewSet

router = routers.DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)

urlpatterns = [
    url(r'^api/', include([
        url(
            r'^register-by-token/(?P<backend>[^/]+)/$',
            'api.views.register_by_access_token',
            name='register_by_access_token',
            ),
        url(r'^', include(router.urls)),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
        ])),
]
