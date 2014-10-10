# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from .decorators import authorized_user, user_is_admin
from .forms import GameForm, ClubForm, CompetitionForm
from .models import Club, Competition, Game, HistoricalScore, Score, Team


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('competition_list_all'))
    else:
        return render(request, 'user/login.html')


@login_required
def competition_list_all(request):
    upcoming_competitions = Competition.objects.filter(
        start_date__gt=timezone.now()
    )
    ongoing_competitions = Competition.objects.filter(
        Q(start_date__lte=timezone.now()) & (Q(end_date__gt=timezone.now()) |
            Q(end_date__isnull=True))
    )
    past_competitions = Competition.objects.filter(
        end_date__lte=timezone.now()
    )

    return render(request, 'competition/list_all.html', {
        'upcoming_competitions': upcoming_competitions,
        'ongoing_competitions': ongoing_competitions,
        'past_competitions': past_competitions
    })


@login_required
@authorized_user
def team_detail(request, competition_slug, team_id):
    competition = get_object_or_404(Competition, slug=competition_slug)
    team = get_object_or_404(Team, pk=team_id)

    head2head = team.get_head2head(competition)
    last_results = team.get_recent_stats(competition, 10)
    longest_streak = team.get_longest_streak(competition)
    current_streak = team.get_current_streak(competition)

    wins = team.get_wins(competition)
    defeats = team.get_defeats(competition)
    games = wins + defeats
    score = team.get_score(competition)

    context = {
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
    }

    return render(request, 'game/team.html', context)


@login_required
def team_general_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    return render(request, 'game/team_general.html', {'team': team})


@login_required
def competition_add(request):
    if request.method == 'POST':
        form = CompetitionForm(request.POST)

        if form.is_valid():
            competition = form.save(request.user)

            return redirect('competition_detail',
                            competition_slug=competition.slug)
    else:
        form = CompetitionForm()

    return render(request, 'competition/new.html', {'form': form})


@login_required
@authorized_user
def competition_detail(request, competition_slug):
    """
    User logged in => homepage
    User not logged => login page
    User not authorized in competition => request access page
    """
    competition = get_object_or_404(Competition, slug=competition_slug)

    latest_results = Game.objects.get_latest(competition)
    score_board = Score.objects.get_score_board(competition)

    context = {
        'latest_results': latest_results,
        'score_board': score_board,
        'competition': competition,
        'user_can_edit_competition': competition.user_has_write_access(request.user),
        'user_is_admin_of_competition': competition.user_is_admin(request.user)
    }

    return render(request, 'competition/detail.html', context)


@login_required
@user_is_admin
def competition_edit(request, competition_slug):
    competition = get_object_or_404(Competition, slug=competition_slug)

    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)

        if form.is_valid():
            competition = form.save(request.user)

            return redirect('competition_detail',
                            competition_slug=competition.slug)
    else:
        form = CompetitionForm(instance=competition)

    return render(request, 'competition/edit.html', {
        'form': form,
        'competition': competition
    })


@login_required
@authorized_user
def competition_detail_score_chart(request, competition_slug, start=0):
    competition = get_object_or_404(Competition, slug=competition_slug)
    score_chart_data = HistoricalScore.objects.get_latest_results_by_team(
        50, competition, start, True
    )
    return HttpResponse(score_chart_data, content_type='application/json')


@login_required
def competition_join(request, competition_slug):
    competition = get_object_or_404(Competition, slug=competition_slug)

    if not competition.user_has_write_access(request.user):
        competition.players.add(request.user)
        messages.add_message(request, messages.SUCCESS, 'Welcome in competition!')

    return redirect(reverse('competition_detail', kwargs={
        'competition_slug': competition.slug
    }))


@login_required
@authorized_user
def game_add(request, competition_slug):
    competition = get_object_or_404(Competition, slug=competition_slug)

    if not competition.is_active():
        messages.add_message(
            request, messages.ERROR, _("The competition is not active.")
        )

        return redirect(reverse('homepage'))

    if request.method == 'POST':
        form = GameForm(request.POST, competition=competition)

        if form.is_valid():
            Game.objects.announce(
                form.cleaned_data['winner'],
                form.cleaned_data['loser'],
                competition
            )

            return redirect(reverse('competition_detail', kwargs={
                'competition_slug': competition.slug
            }))
    else:
        form = GameForm(competition=competition)

    return render(request, 'game/add.html', {
        'form': form,
        'competition': competition,
    })


@login_required
@authorized_user
@require_POST
def game_remove(request, competition_slug):

    competition = get_object_or_404(Competition, slug=competition_slug)

    if not competition.is_active():
        messages.add_message(
            request, messages.ERROR, _("The competition is not active.")
        )

        return redirect(reverse('homepage'))

    game_id = request.POST['game_id']
    game = get_object_or_404(Game, pk=game_id)

    last_game = Game.objects.get_latest(competition)[0]

    if last_game.id == game.id:
        Game.objects.delete(game, competition)

        # Remove the team score from the competition if it was its only game
        teams = [last_game.winner, last_game.loser]
        for team in teams:
            count = Game.objects.filter(Q(winner=team) | Q(loser=team), competitions=competition).count()
            if count == 0:
                Score.objects.filter(competition=competition, team=team).delete()

        messages.add_message(request, messages.SUCCESS, 'Last game was deleted.')
    else:
        messages.add_message(request, messages.ERROR, 'Trying to delete a game that is not the last.')

    return redirect('game.views.competition_detail', competition_slug=competition_slug)

@login_required
def club_add(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)

        if form.is_valid():
            club = form.save()

            return redirect('club_detail',
                            club_slug=club.slug)
    else:
        form = ClubForm()

    return render(request, 'club/new.html', {'form': form})


@login_required
def club_detail(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug)

    context = {
        'club': club,
    }

    return render(request, 'club/detail.html', context)


@login_required
def club_list_all(request):
    return render(request, 'club/list_all.html')
