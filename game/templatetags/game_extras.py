from django import template
from django.template.defaultfilters import floatformat

from ..models import Club, Competition


register = template.Library()


@register.inclusion_tag('competition/_list.html', takes_context=True)
def competitions_list(context):
    request = context['request']
    return {
        'competitions': Competition.objects.get_visible_for_user(request.user).order_by('name')
    }


@register.filter
def as_percentage_of(part, whole):
    try:
        return floatformat(float(part) / whole * 100, 2) + '%'
    except (ValueError, ZeroDivisionError):
        return ""


@register.inclusion_tag('club/_list.html')
def all_clubs_list():
    return {
        'clubs': Club.objects.all().order_by('name')
    }
