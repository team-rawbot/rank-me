import json
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from social.apps.django_app.utils import psa
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from game.models import Competition, Team

from .serializers import CompetitionSerializer, \
    TeamSerializer, UserSerializer


@psa('social:complete')
def register_by_access_token(request, backend):
    backend = request.backend
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
    return HttpResponse(data_json, content_type='application/json')


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API users endpoint
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None, **kwargs):
        queryset = get_user_model().objects.all()

        current_user = request.user
        if current_user.is_authenticated() and pk == 'current':
            pk = current_user.id

        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
