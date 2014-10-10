from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from .models import Competition, Club


def authorized_user(func):
    """
    Check that user has read access to the competition
    """
    def decorator(request, *args, **kwargs):
        competition = get_object_or_404(Competition,
                                        slug=kwargs['competition_slug'])

        if competition.user_has_write_access(request.user):
            return func(request, *args, **kwargs)

        return render(request, 'competition/no_access.html', {
            'competition': competition,
        })

    return decorator


def user_is_admin(func):
    """
    Check that user is admin of competition
    """
    def decorator(request, *args, **kwargs):
        competition = get_object_or_404(Competition,
                                        slug=kwargs['competition_slug'])

        if competition.user_is_admin(request.user):
            return func(request, *args, **kwargs)

        raise PermissionDenied()

    return decorator

def user_can_edit_club(func):
    """
    Check that user can edit club
    """
    def decorator(request, *args, **kwargs):
        club = get_object_or_404(Club, slug=kwargs['club_slug'])

        if club.user_is_admin(request.user):
            return func(request, *args, **kwargs)

        raise PermissionDenied()

    return decorator
