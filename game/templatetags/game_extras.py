from django import template

from ..models import Competition

register = template.Library()
from django.template.defaultfilters import floatformat


@register.inclusion_tag('competition/_list.html', takes_context = True)
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
