from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from . import stats
from .decorators import authorized_user, user_is_admin
from .forms import GameForm, CompetitionForm
from .models import Competition, Game, HistoricalScore, Score


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
def player_detail(request, competition_slug, player_id):
    competition = get_object_or_404(Competition, slug=competition_slug)
    player = get_object_or_404(get_user_model(), pk=player_id)

    head2head = competition.get_head2head(player)
    last_results = competition.get_last_games_stats(player, 10)
    longest_streak = competition.get_longest_streak(player)
    current_streak = competition.get_current_streak(player)

    wins = competition.get_wins(player)
    defeats = competition.get_defeats(player)
    games = wins + defeats
    score = competition.get_score(player)

    context = {
        'player': player,
        'head2head': head2head,
        'last_results': last_results,
        'longest_streak': longest_streak,
        'current_streak': current_streak,
        'games': games,
        'wins': wins,
        'defeats': defeats,
        'score': score,
        'competition': competition,
        'stats_per_week': stats.get_stats_per_week(player, Game.objects.all()),
    }

    return render(request, 'game/player.html', context)


@login_required
def player_general_detail(request, player_id):
    player = get_object_or_404(get_user_model(), pk=player_id)

    return render(request, 'game/player_general.html', {'player': player})


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
    competition.add_user_access(request.user)
    messages.add_message(request, messages.SUCCESS, 'Welcome in competition!')

    return redirect(reverse('competition_detail', kwargs={
        'competition_slug': competition.slug
    }))


@login_required
@require_POST
def competition_leave(request, competition_slug):
    competition = get_object_or_404(Competition, slug=competition_slug)
    competition.remove_user_access(request.user)
    messages.add_message(request, messages.SUCCESS, 'You left the competition')

    return redirect(reverse('homepage'))


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

        # Remove the player score from the competition if it was its only game
        players = [last_game.winner, last_game.loser]
        for player in players:
            count = Game.objects.filter(Q(winner=player) | Q(loser=player), competitions=competition).count()
            if count == 0:
                Score.objects.filter(competition=competition, player=player).delete()

        messages.add_message(request, messages.SUCCESS, 'Last game was deleted.')
    else:
        messages.add_message(request, messages.ERROR, 'Trying to delete a game that is not the last.')

    return redirect('game.views.competition_detail', competition_slug=competition_slug)
