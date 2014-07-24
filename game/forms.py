from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Competition


class GameForm(forms.Form):
    winner = forms.ModelChoiceField(
        queryset=get_user_model().objects.all().order_by('username')
    )
    loser = forms.ModelChoiceField(
        queryset=get_user_model().objects.all().order_by('username')
    )

    def __init__(self, *args, **kwargs):
        competition = kwargs.pop('competition', None)

        super(GameForm, self).__init__(*args, **kwargs)

        if competition is not None:
            self.fields['winner'].queryset = competition.competitors.all().order_by('username')
            self.fields['loser'].queryset = competition.competitors.all().order_by('username')

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
        fields = ('name', 'description', 'start_date', 'end_date')
