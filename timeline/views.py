from django.shortcuts import render
from game.models import Competition
from .models import Event

def index(request):
    if not request.user.is_authenticated():
        # Public homepage
        return render(request, 'user/login.html')

    # Private homepage
    context = {
        'events': Event.objects.get_all_for_user(request.user),
        'competitions': Competition.objects.get_visible_for_user(request.user),
        'clubs': request.user.clubs.all()
    }
    return render(request, 'timeline/index.html', context)
