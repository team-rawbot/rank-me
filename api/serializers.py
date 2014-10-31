from django.contrib.auth import get_user_model
from rest_framework import serializers

from game.models import Competition, Team, Game, Score


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
    winner_id = serializers.WritableField(required=False, write_only=True)
    loser_id = serializers.WritableField(required=False, write_only=True)
    competition_id = serializers.WritableField(required=False, write_only=True)

    winner = serializers.WritableField(required=False, read_only=True)
    loser = serializers.WritableField(required=False, read_only=True)
    competitions = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = Game


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    team = serializers.RelatedField()
    competition = serializers.RelatedField()

    class Meta:
        model = Score
        fields = ('id', 'team', 'competition', 'score', 'stdev')


class HistoricalScoreSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    team = serializers.IntegerField()

    score = serializers.FloatField()
    stdev = serializers.FloatField()
    position = serializers.IntegerField()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name')
