from rest_framework import viewsets

from game.models import Competition

from .serializers import CompetitionSerializer


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

