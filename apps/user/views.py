from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import itertools

from .forms import User, UserProfileForm, UserForm


@login_required
def index(request, user_id=None):
    if user_id:
        displayed_user = get_object_or_404(User, pk=user_id)
    else:
        displayed_user = request.user

    profile = displayed_user.profile

    scores = request.user.scores.all()
    return render(request, 'user/profile.html', {
        'user': request.user,
        'profile': request.user.profile,
        'scores': scores,
        'can_edit': displayed_user == request.user
    })


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('profile'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'user/edit.html', {'user_form': user_form, 'profile_form': profile_form})
