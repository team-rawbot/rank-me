from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import itertools



@login_required
def index(request):
    scores = itertools.chain.from_iterable([t.scores.all() for t in request.user.teams.all()])
    return render(request, 'user/profile.html', {
        'user': request.user,
        'profile': request.user.get_profile(),
        'scores': scores
    })


@login_required
def edit(request):
    return render(request, 'user/edit.html')
