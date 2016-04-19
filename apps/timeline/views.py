from django.shortcuts import render

from .models import Event


def index(request):
    if not request.user.is_authenticated():
        # Public homepage
        return render(request, 'user/login.html')

    # Private homepage
    context = {
        'events': Event.objects.get_all_for_player(request.user)[:50],
        'clubs': request.user.clubs.all()
    }

    return render(request, 'timeline/index.html', context)
