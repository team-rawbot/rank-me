from rest_framework import serializers

from game.models import Competition, Team, Game
from django.contrib.auth import get_user_model


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'slug')


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.RelatedField(many=True)
    name = serializers.Field(source='get_name')
    competitions = serializers.Field(source='get_competitions')

    class Meta:
        model = Team
        fields = ('id', 'name', 'competitions', 'users')


class GameSerializer(serializers.Serializer):
    winner_id = serializers.WritableField(required=False)
    loser_id = serializers.WritableField(required=False)
    competition_id = serializers.WritableField(required=False)

    winner = serializers.WritableField(required=False)
    loser = serializers.WritableField(required=False)
    competition = serializers.WritableField(required=False)

