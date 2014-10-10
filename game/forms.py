from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Competition, Club, Team


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_profile().full_name()


class GameForm(forms.Form):
    # values overridden in __init__ !
    winner = forms.ModelChoiceField(queryset=Team.objects.none())
    loser = forms.ModelChoiceField(queryset=Team.objects.none())

    def __init__(self, *args, **kwargs):
        self.competition = kwargs.pop('competition')
        super(GameForm, self).__init__(*args, **kwargs)

        queryset = get_user_model().objects.filter(
            id__in=self.competition.players.all()
        ).extra(
            select={'lower_first': 'lower(first_name)'}
        ).order_by('lower_first')

        self.fields['winner'].queryset = queryset
        self.fields['loser'].queryset = queryset

    def save(self):
        Game.objects.announce(self.winner, self.loser, self.competition)

    def clean(self):
        cleaned_data = super(GameForm, self).clean()
        winner = cleaned_data.get('winner', None)
        loser = cleaned_data.get('loser', None)

        if None not in [winner, loser] and winner == loser:
            raise ValidationError(
                _("Winner and loser can't be the same player!"),
                code="same_players"
            )

        return cleaned_data


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ('name', 'description', 'players', 'start_date', 'end_date')

    def save(self, creator):
        competition = super(CompetitionForm, self).save(commit=False)
        competition.creator = creator
        competition.save()

        return competition


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'description', 'members')
