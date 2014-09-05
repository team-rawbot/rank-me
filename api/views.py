import json
from django.contrib.auth import login, get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from social.apps.django_app.utils import strategy
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from api.serializers import TeamSerializer

from game.models import Competition, Team, Game

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


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@api_view(['POST'])
def add_result(request):
    errors = []
    try:
        competition = Competition.objects.get(slug=request.DATA['competition'])
    except MultiValueDictKeyError:
        errors.append('No competition given')
    except Competition.DoesNotExist as e:
        competition = None
        errors.append('Competition not found')

    try:
        winner = get_user_model().objects.get(username=request.DATA['winner'])
    except MultiValueDictKeyError:
        errors.append('No winner given')
    except get_user_model().DoesNotExist as e:
        winner = None
        errors.append('Winner not found')

    try:
        looser = get_user_model().objects.get(username=request.DATA['looser'])
    except MultiValueDictKeyError:
        errors.append('No looser given')
    except get_user_model().DoesNotExist as e:
        looser = None
        errors.append('Looser not found')

    if errors:
        payload = {
            'status': 'error',
            'errors': errors
        }
        code = status.HTTP_400_BAD_REQUEST
    else:
        Game.objects.announce(
            winner,
            looser,
            competition
        )
        payload = {'status': 'success', }
        code = status.HTTP_201_CREATED

    return Response(payload, status=code)
