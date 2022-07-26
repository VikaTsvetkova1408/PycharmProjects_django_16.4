import re
from django import template

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
