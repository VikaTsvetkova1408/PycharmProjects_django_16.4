from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .models import Post


@receiver(m2m_changed, sender=Post.category.through, dispatch_uid='notify_subscribers_signal')
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        context = {'post': instance}
        recepients = set()
        for category in instance.category.all():
            for subscriber in category.subscribers.all():
                recepients.add(subscriber.email)

        message = get_template('email_notify.html').render(context)
        msg = EmailMessage('Yay! New post!',
                           message,
                           'newsletter@onlynews.xxx',
                           list(recepients))
        msg.content_subtype = 'html'
        msg.send()
