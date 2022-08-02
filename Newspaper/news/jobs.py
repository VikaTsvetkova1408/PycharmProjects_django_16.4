from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .models import Post, Category


def post_weekly_digest():
    context = {}
    for category in Category.objects.all():
        context['category'] = category
        context['posts'] = category.post_set.filter(timestamp__gte=datetime.utcnow() - timedelta(days=7))
        for subscriber in category.subscribers.all():
            message = get_template('email_digest.html').render(context | {'user': subscriber})
            msg = EmailMessage('Weekly Posts Digest!',
                               message,
                               'newsletter@onlynews.xxx',
                               [subscriber.email])
            msg.content_subtype = 'html'
            msg.send()

