import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class GameForm(forms.Form):
    winner = forms.ModelChoiceField(queryset=get_user_model().objects.all().order_by('username'))
    loser = forms.ModelChoiceField(queryset=get_user_model().objects.all().order_by('username'))

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

class CompetitionForm(forms.Form):
    name = forms.CharField(label='Name')
    description = forms.CharField(label='Description')
    start_date = forms.DateField(initial=datetime.date.today)
    end_date = forms.DateField(initial=datetime.date.today)

    def clean(self):
        cleaned_data = super(CompetitionForm, self).clean()
        name = cleaned_data.get('name', None)

        if name is None:
            raise ValidationError(_("Name is mandatory"))

        return cleaned_data
