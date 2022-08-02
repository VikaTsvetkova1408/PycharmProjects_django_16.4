from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mass_mail, send_mail
from .models import Post, PostCategory


@receiver(m2m_changed, sender=Post.category.through, dispatch_uid='notify_subscribers_signal')
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        recepients = set()
        for category in instance.category.all():
            for subscriber in category.subscribers.all():
                recepients.add(subscriber.email)
        send_mail('Yay! New post!',
                  'Go check it',
                  'newsletter@onlynews.xxx',
                  list(recepients))
