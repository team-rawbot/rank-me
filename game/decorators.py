from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Competition

def authorized_user(func):
    """
    Check that user has read access to the competition
    """
    def decorator(request, *args, **kwargs):
        competition = get_object_or_404(Competition, slug=kwargs['competition_slug'])

        if competition.user_has_write_access(request.user):
            return func(request, *args, **kwargs)

        return HttpResponse('Unauthorized', status=401)

    return decorator
