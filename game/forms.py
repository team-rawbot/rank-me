from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class GameForm(forms.Form):
    winner = forms.ModelChoiceField(queryset=User.objects.all())
    loser = forms.ModelChoiceField(queryset=User.objects.all())

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
