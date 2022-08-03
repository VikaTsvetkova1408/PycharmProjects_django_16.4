import re
from django import template
from django.contrib.sites.models import Site

register = template.Library()

BADWORDS = ['carrot', 'radish']


@register.filter(name='profanity')
def profanity(value):
    """
    Very basic profanity filter
    """

    result = value
    for word in BADWORDS:
        result = re.sub(word, '#' * len(word), result, flags=re.IGNORECASE)
    return result


@register.filter
def site_domain(path):
    current_site = Site.objects.get_current()
    return current_site.domain + path
