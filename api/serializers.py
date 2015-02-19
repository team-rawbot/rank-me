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


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'winner', 'loser')
