from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .forms import GameForm
from .models import Game, Team, HistoricalScore


def index(request):
    """
    User logged in => homepage
    User not logged => login page
    """
    if request.user.is_authenticated():
        latest_results = Game.objects.get_latest()
        score_board = Team.objects.get_score_board()
        score_chart_data = HistoricalScore.objects.get_latest_results_by_team(50, True)

        context = {
            'latest_results': latest_results,
            'score_board': score_board,
            'score_chart_data': score_chart_data,
        }

        return render(request, 'game/index.html', context)
    else:
        return render(request, 'user/login.html')


def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    return render(request, 'game/detail.html', {'game': game})


def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    context = {
        'team': team,
        'head2head': team.get_head2head(),
        'last_results': team.get_recent_stats(10),
        'longest_streak': team.get_longest_streak(),
        'stats_per_week': team.get_stats_per_week()
    }

    return render(request, 'game/team.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
            Game.objects.announce(
                form.cleaned_data['winner'],
                form.cleaned_data['loser']
            )

            return redirect('game_index')
    else:
        form = GameForm()

    return render(request, 'game/add.html', {'form': form})
