from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Competition

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = "%s %s" % (obj.first_name, obj.last_name)

        if not full_name.strip():
            display_name = obj.username
        else:
            display_name = full_name

        return display_name.title()


class GameForm(forms.Form):
    winner = UserChoiceField(
        queryset = get_user_model().objects.all().extra(select={'lower_first': 'lower(first_name)'}).order_by('lower_first'),
        empty_label = ''
    )
    loser = UserChoiceField(
        queryset = get_user_model().objects.all().extra(select={'lower_first': 'lower(first_name)'}).order_by('lower_first'),
        empty_label = ''
    )

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
