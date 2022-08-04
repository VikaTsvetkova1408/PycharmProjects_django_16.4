"""
Celery Tasks
"""

from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .models import Post, Category


@shared_task()
def weekly_digest():
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


@shared_task()
def send_mail_to_subscribers(post_id):
    post = Post.objects.get(pk=post_id)
    context = {'post': post}
    recepients = set()
    for category in post.category.all():
        for subscriber in category.subscribers.all():
            recepients.add(subscriber.email)

    message = get_template('email_notify.html').render(context)
    msg = EmailMessage('Yay! New post!',
                       message,
                       'newsletter@onlynews.xxx',
                       list(recepients))
    msg.content_subtype = 'html'
    msg.send()

