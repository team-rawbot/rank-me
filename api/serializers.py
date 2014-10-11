from rest_framework import serializers

from game.models import Competition, Team, Game


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

