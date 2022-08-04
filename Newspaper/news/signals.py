from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .models import Post
from .tasks import send_mail_to_subscribers


@receiver(m2m_changed, sender=Post.category.through, dispatch_uid='notify_subscribers_signal')
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_mail_to_subscribers.apply_async([instance.id], countdown=10)
