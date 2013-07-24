from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from game.models import Game, Rank, GameForm


def index(request):
    latest_results = Game.objects.get_latest()
    score_board = Rank.objects.get_score_board()
    context = {
        'latest_results': latest_results,
        'score_board': score_board
    }
    return render(request, 'game/index.html', context)


def detail(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404
    return render(request, 'game/detail.html', {'game': game})


def add(request):
    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('game_index')
    else:
        form = GameForm()

    return render(request, 'game/add.html', {'form': form})
