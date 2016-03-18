from django.contrib.auth import get_user_model
from rest_framework import serializers

from game.models import Competition, Game, Score


class ScoreSerializer(serializers.ModelSerializer):
    player_name = serializers.ReadOnlyField(source='get_player_name')
    player_avatar = serializers.ReadOnlyField(source='get_player_avatar')
    player_id = serializers.ReadOnlyField()

    class Meta:
        model = Score
        fields = ('id', 'player_id', 'player_name', 'player_avatar', 'score', 'stdev')


class CompetitionSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)

    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'slug', 'scores')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name')


class GameSerializer(serializers.Serializer):
    winner_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    loser_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    competition_id = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all())

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'winner_id': obj.winner_id,
            'loser_id': obj.loser_id,
            'competition_id': obj.competition_id,
        }

    def create(self, validated_data):
        winner = validated_data['winner_id']
        loser = validated_data['loser_id']
        competition = validated_data['competition_id']

        return Game.objects.announce(winner, loser, competition)

    # Must implement all abstract methods but we don't want to implement the update method
    def update(self, instance, validated_data):
        pass
