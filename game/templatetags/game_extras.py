from django import template

from ..models import Competition

register = template.Library()
from django.template.defaultfilters import floatformat


@register.inclusion_tag('competition/_list.html')
def competitions_list():
    return {
        'competitions': Competition.objects.all().order_by('name')
    }

@register.filter
def as_percentage_of(part, whole):
    try:
        return floatformat(float(part) / whole * 100, 2) + '%'
    except (ValueError, ZeroDivisionError):
        return ""
