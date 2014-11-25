from django.shortcuts import render
from game.models import Competition
from .models import Event

def index(request):
    if not request.user.is_authenticated():
        # Public homepage
        return render(request, 'user/login.html')

    # Private homepage
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'timeline/index.html', context)
