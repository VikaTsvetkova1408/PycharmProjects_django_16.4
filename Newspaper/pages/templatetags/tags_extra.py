from django import template

register = template.Library()

BADWORDS = ['carrot', 'radish']


@register.filter(name='profanity')
def profanity(value):
    """
    Very basic profanity filter
    """

    # TODO use regexp
    result = value
    for word in BADWORDS:
        result = result.replace(word, '#' * len(word))
    return result
