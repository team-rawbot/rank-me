from django.http import Http404
from django.shortcuts import render
from trueskill import Rating, rate_1vs1
from game.models import Game

def index(request):
    latest_results = Game.objects.all().order_by('-date')[:20]
    context = {'latest_results': latest_results}
    return render(request, 'game/index.html', context)

def detail(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404
    return render(request, 'game/detail.html', {'game': game})
