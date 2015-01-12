from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .forms import UserProfileForm, UserForm


@login_required
def index(request):
    my_teams = request.user.teams.all()
    competition_datas = []

    for team in my_teams:
        for competition in team.get_competitions():
            head2head = team.get_head2head(competition)
            last_results = team.get_recent_stats(competition, 10)
            longest_streak = team.get_longest_streak(competition)
            current_streak = team.get_current_streak(competition)

            wins = team.get_wins(competition)
            defeats = team.get_defeats(competition)
            games = wins + defeats
            score = team.get_score(competition)

            competition_datas.append({
                'team': team,
                'head2head': head2head,
                'last_results': last_results,
                'longest_streak': longest_streak,
                'current_streak': current_streak,
                'games': games,
                'wins': wins,
                'defeats': defeats,
                'score': score,
                'competition': competition,
                'stats_per_week': team.get_stats_per_week(),
            })

    context = {
        'user': request.user,
        'profile': request.user.get_profile(),
        'competition_datas': competition_datas,
    }

    return render(request, 'user/profile.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST,
            instance=request.user.get_profile()
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('profile'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.get_profile())

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'user/edit.html', context)
