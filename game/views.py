from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .forms import GameForm, CompetitionForm
from .models import Competition, Game, HistoricalScore, Score, Team


def index(request):
    """
    User logged in => homepage
    User not logged => login page
    """
    if request.user.is_authenticated():
        default_competition = Competition.objects.get_default_competition()

        latest_results = Game.objects.get_latest(default_competition)
        score_board = Score.objects.get_score_board(default_competition)
        score_chart_data = HistoricalScore.objects.get_latest_results_by_team(
            50, default_competition, True
        )

        context = {
            'latest_results': latest_results,
            'score_board': score_board,
            'score_chart_data': score_chart_data,
            'competitions': Competition.objects.all(),
        }

        return render(request, 'game/index.html', context)
    else:
        return render(request, 'user/login.html')


@login_required
def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    return render(request, 'game/detail.html', {'game': game})


@login_required
def team(request, team_id):
    default_competition = Competition.objects.get_default_competition()

    team = get_object_or_404(Team, pk=team_id)
    head2head = team.get_head2head(default_competition)
    last_results = team.get_recent_stats(default_competition, 10)
    longest_streak = team.get_longest_streak(default_competition)

    wins = team.get_wins(default_competition)
    defeats = team.get_defeats(default_competition)
    score = team.get_score(default_competition)

    context = {
        'team': team,
        'head2head': head2head,
        'last_results': last_results,
        'longest_streak': longest_streak,
        'wins': wins,
        'defeats': defeats,
        'score': score
    }

    return render(request, 'game/team.html', context)


@login_required
def create_competition(request):
    if request.method == 'POST':
        form = CompetitionForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('game_index')
    else:
        form = CompetitionForm()

    return render(request, 'competition/new.html', {'form': form})


@login_required
def view_competition(request, slug):
    pass


@login_required
def add(request):
    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
            Game.objects.announce(
                form.cleaned_data['winner'],
                form.cleaned_data['loser'],
                Competition.objects.get_default_competition()
            )

            return redirect('game_index')
    else:
        form = GameForm()

    return render(request, 'game/add.html', {'form': form})
