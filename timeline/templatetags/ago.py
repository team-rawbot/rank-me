from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def ago(date):
    ago = timesince(date)
    # selects only the first part of the returned string
    return ago.split(",")[0] + " ago"
