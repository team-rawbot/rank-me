from django import template

from ..models import Competition

register = template.Library()


@register.inclusion_tag('competition/_list.html')
def competitions_list():
    return {
        'competitions': Competition.objects.all().order_by('name')
    }
