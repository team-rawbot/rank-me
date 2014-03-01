from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .forms import GameForm
from .models import Game, Team


def index(request):
    latest_results = Game.objects.get_latest()
    score_board = Team.objects.get_score_board()
    context = {
        'latest_results': latest_results,
        'score_board': score_board
    }
    return render(request, 'game/index.html', context)


def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    return render(request, 'game/detail.html', {'game': game})


def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    head2head = team.get_head2head()
    last_results = team.get_last_results(10)
    longest_streak = team.get_longest_streak()

    context = {
        'team' : team,
        'head2head' : head2head,
        'last_results' : last_results,
        'longest_streak' : longest_streak,
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
