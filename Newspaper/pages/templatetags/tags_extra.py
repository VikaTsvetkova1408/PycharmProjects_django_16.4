from django import template

register = template.Library()

BADWORDS = ['carrot', 'radish']


@register.filter(name='profanity')
def profanity(value):

    return value.replace('')
