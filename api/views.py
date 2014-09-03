import json
from django.contrib.auth import login
from django.http import HttpResponse
from social.apps.django_app.utils import strategy
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from api.serializers import TeamSerializer

from game.models import Competition, Team

from .serializers import CompetitionSerializer


@strategy('social:complete')
def register_by_access_token(request, backend):
    backend = request.strategy.backend
    token = {
        'oauth_token': request.GET.get('oauth_token'),
        'oauth_token_secret': request.GET.get('oauth_token_secret'),
    }

    user = backend.do_auth(token)
    token, created = Token.objects.get_or_create(user=user)

    data = {
        'api_token': token.key
    }

    data_json = json.dumps(data)
    return HttpResponse(data_json, mimetype='application/json')


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

