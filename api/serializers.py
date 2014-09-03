from rest_framework import serializers

from game.models import Competition


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = ('name', 'description', 'slug')
