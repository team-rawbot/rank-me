from rest_framework import serializers

from game.models import Competition, Team


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = ('name', 'description', 'slug')


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.RelatedField(many=True)
    name = serializers.Field(source='get_name')
    competitions = serializers.Field(source='get_competitions')

    class Meta:
        model = Team
        fields = ('name', 'competitions', 'users',)
