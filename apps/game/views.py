from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from . import stats
from .decorators import authorized_user, user_is_admin, user_can_edit_club
from .forms import GameForm, ClubForm, CompetitionForm
from .models import Club, Competition, Game, Score


@login_required
def competition_list_all(request):
    return render(request, 'competition/list_all.html', {
        'upcoming_competitions': Competition.upcoming_objects.all(),
        'ongoing_competitions': Competition.ongoing_objects.all(),
        'past_competitions': Competition.past_objects.all()
    })


@login_required
@authorized_user
def player_detail(request, competition_slug, player_id):
    competition = get_object_or_404(Competition, slug=competition_slug)
    player = get_object_or_404(get_user_model(), pk=player_id)

    head2head = stats.get_head2head(player, competition)
    last_results = stats.get_last_games_stats(player, competition, 10)
    longest_streak = stats.get_longest_streak(player, competition)
    current_streak = stats.get_current_streak(player, competition)

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
        'stats_per_week': stats.get_stats_per_week(player),
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

    latest_results = competition.get_latest_games()
    score_board = competition.get_score_board()

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
    score_chart_data = stats.get_latest_results_by_player(
        competition, 50, int(start), True
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

    if request.method == 'POST':
        form = GameForm(request.POST, competition=competition)

        if form.is_valid():
            winner, loser = form.cleaned_data['winner'], form.cleaned_data['loser']
            game = competition.add_game(winner, loser)
            messages.add_message(
                request, messages.SUCCESS, _('Game %s added.') % game
            )

            # save_add is set if the user clicked on "add another"
            if 'save_add' in request.POST:
                redirect_route = 'game_add'
                redirect_qs = '?winner={winner}&loser={loser}'.format(
                    winner=winner.id, loser=loser.id
                )
            else:
                redirect_route = 'competition_detail'
                redirect_qs = ''

            return redirect(reverse(redirect_route, kwargs={
                'competition_slug': competition.slug
            }) + redirect_qs)
    else:
        selected_winner, selected_loser = request.GET.get('winner'), request.GET.get('loser')
        form = GameForm(competition=competition, initial={
            'winner': selected_winner,
            'loser': selected_loser
        })

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

    last_game = competition.get_latest_games()[0]

    if last_game.id == game.id:
        game.delete()

        # Remove the player score from the competition if it was its only game
        players = [last_game.winner, last_game.loser]
        for player in players:
            count = Game.objects.filter(Q(winner=player) | Q(loser=player), competition=competition).count()
            if count == 0:
                Score.objects.filter(competition=competition, player=player).delete()

        messages.add_message(request, messages.SUCCESS, 'Last game was deleted.')
    else:
        messages.add_message(request, messages.ERROR, 'Trying to delete a game that is not the last.')

    return redirect('game.views.competition_detail', competition_slug=competition_slug)

@login_required
def club_add(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)

        if form.is_valid():
            club = form.save(request.user)

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
        'user_can_edit_club': club.user_is_admin(request.user)
    }

    return render(request, 'club/detail.html', context)


@login_required
def club_list_all(request):
    return render(request, 'club/list_all.html')


@login_required
@user_can_edit_club
def club_edit(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug)

    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)

        if form.is_valid():
            club = form.save(request.user)

            return redirect('club_detail',
                            club_slug=club.slug)
    else:
        form = ClubForm(instance=club)

    context = {
        'form': form
    }

    return render(request, 'club/edit.html', context)
