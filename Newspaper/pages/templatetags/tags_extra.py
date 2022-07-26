from django import template

register = template.Library()

BADWORDS = ['carrot', 'radish']


@register.filter(name='profanity')
def profanity(value):
    result = value
    for word in BADWORDS:
        result = result.replace(word, '#' * len(word))
    return result
