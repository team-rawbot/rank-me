from django.contrib.auth import get_user_model
from rest_framework import serializers

from game.models import Competition, Team, Game


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'slug')


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='get_name')

    class Meta:
        model = Team
        fields = ('id', 'name', 'users', 'competitions')


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name')


class GameSerializer(serializers.Serializer):
    winner_id = serializers.IntegerField(required=True)
    loser_id = serializers.IntegerField(required=True)
    competition_id = serializers.IntegerField(required=True)

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'winner_id': obj.winner_id,
            'loser_id': obj.winner_id,
            'competition_ids': obj.competitions.values_list('id', flat=True),
        }

    def create(self, validated_data):
        winner = Team.objects.get(pk=validated_data['winner_id'])
        loser = Team.objects.get(pk=validated_data['loser_id'])
        competition = Competition.objects.get(pk=validated_data['competition_id'])

        return Game.objects.announce(winner.users.all()[0], loser.users.all()[0], competition)

    def update(self, instance, validated_data):
        pass
