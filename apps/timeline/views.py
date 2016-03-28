from django.shortcuts import render

from ..game.models import Competition
from .models import Event


def index(request):
    if not request.user.is_authenticated():
        # Public homepage
        return render(request, 'user/login.html')

    # Private homepage
    context = {
        'events': Event.objects.get_all_for_player(request.user)[:50],
        'ongoing_competitions': Competition.ongoing_objects
                                           .get_visible_for_user(request.user),
        'past_competitions': Competition.past_objects
                                        .get_visible_for_user(request.user)
    }
    return render(request, 'timeline/index.html', context)
