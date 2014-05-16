from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect

from .forms import GameForm, CompetitionForm
from .models import Competition, Game, HistoricalScore, Score, Team


@login_required
def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('competition_detail', kwargs={
            'competition_slug': 'default-competition'
        }))
    else:
        return render('user/login.html')


@login_required
def game_detail(request, competition_slug, game_id):
    game = get_object_or_404(Game, pk=game_id)

    return render(request, 'game/detail.html', {'game': game})


@login_required
def team_detail(request, competition_slug, team_id):
    competition = get_object_or_404(Competition, slug=competition_slug)
    team = get_object_or_404(Team, pk=team_id)

    head2head = team.get_head2head(competition)
    last_results = team.get_recent_stats(competition, 10)
    longest_streak = team.get_longest_streak(competition)

    wins = team.get_wins(competition)
    defeats = team.get_defeats(competition)
    score = team.get_score(competition)

    context = {
        'team': team,
        'head2head': head2head,
        'last_results': last_results,
        'longest_streak': longest_streak,
        'wins': wins,
        'defeats': defeats,
        'score': score,
        'competition': competition,
    }

    return render(request, 'game/team.html', context)


@login_required
def competition_add(request):
    if request.method == 'POST':
        form = CompetitionForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('game_index')
    else:
        form = CompetitionForm()

    return render(request, 'competition/new.html', {'form': form})


@login_required
def competition_detail(request, competition_slug):
    """
    User logged in => homepage
    User not logged => login page
    """
    competition = get_object_or_404(Competition, slug=competition_slug)

    latest_results = Game.objects.get_latest(competition)
    score_board = Score.objects.get_score_board(competition)
    score_chart_data = HistoricalScore.objects.get_latest_results_by_team(
        50, competition, True
    )

    context = {
        'latest_results': latest_results,
        'score_board': score_board,
        'score_chart_data': score_chart_data,
        'competition': competition,
    }

    return render(request, 'competition/detail.html', context)


@login_required
def game_add(request, competition_slug):
    competition = get_object_or_404(Competition, slug=competition_slug)

    if request.method == 'POST':
        form = GameForm(request.POST)

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
        form = GameForm()

    return render(request, 'game/add.html', {
        'form': form,
        'competition': competition,
    })
