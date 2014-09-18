from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Competition, Game


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('winner', 'loser')

    def __init__(self, *args, **kwargs):
        competition = kwargs.pop('competition')
        super(GameForm, self).__init__(*args, **kwargs)

        queryset = get_user_model().objects.filter(id__in=competition.players.all()).order_by('username')

        self.fields['winner'].queryset = queryset
        self.fields['loser'].queryset = queryset


    def clean(self):
        cleaned_data = super(GameForm, self).clean()
        winner = cleaned_data.get('winner', None)
        loser = cleaned_data.get('loser', None)

        if winner is not None and loser is not None and winner == loser:
            raise ValidationError(
                _("Winner and loser can't be the same player!"),
                code="same_players"
            )

        return cleaned_data


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ('name', 'description', 'players', 'start_date', 'end_date')
