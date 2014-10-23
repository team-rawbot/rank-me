import json
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from social.apps.django_app.utils import psa
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_extensions.mixins import NestedViewSetMixin

from game.models import Competition, Team, Game, Score

from .serializers import CompetitionSerializer, TeamSerializer, GameSerializer, ScoreSerializer


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


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    """
    model = Competition
    serializer_class = CompetitionSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    model = Team
    serializer_class = TeamSerializer


class TeamPerCompetitionViewSet(NestedViewSetMixin, TeamViewSet):
    pass


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Games to be viewed or edited.
    """
    model = Game
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        """
        API endpoint that allows to add a new result
        """

        errors = []
        winner = None
        loser = None
        competition = None

        try:
            if 'winner_id' in request.DATA:
                winner = get_user_model().objects.get(id=request.DATA['winner_id'])
            else:
                winner = get_user_model().objects.get(username=request.DATA['winner'])
        except MultiValueDictKeyError:
            errors.append('No winner given')
        except get_user_model().DoesNotExist as e:
            errors.append('Winner not found')

        try:
            if 'loser_id' in request.DATA:
                loser = get_user_model().objects.get(id=request.DATA['loser_id'])
            else:
                loser = get_user_model().objects.get(username=request.DATA['loser'])
        except MultiValueDictKeyError:
            errors.append('No loser given')
        except get_user_model().DoesNotExist as e:
            errors.append('Loser not found')

        try:
            if 'competition_id' in request.DATA:
                competition = Competition.objects.get(id=request.DATA['competition_id'])
            else:
                competition = Competition.objects.get(slug=request.DATA['competition'])
        except MultiValueDictKeyError:
            errors.append('No competition given')
        except Competition.DoesNotExist as e:
            errors.append('Competition not found')

        if errors:
            payload = {
                'status': 'error',
                'errors': errors
            }
            code = status.HTTP_400_BAD_REQUEST
        else:
            Game.objects.announce(
                winner,
                loser,
                competition
            )
            payload = {'status': 'success', }
            code = status.HTTP_201_CREATED

        return Response(payload, status=code)


class GamePerCompetitionViewSet(NestedViewSetMixin, GameViewSet):
    pass


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows scores to be viewed or edited.
    """
    model = Score
    serializer_class = ScoreSerializer


class ScorePerCompetitionViewSet(NestedViewSetMixin, ScoreViewSet):
    pass
