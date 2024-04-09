from celery.app import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, User
from django.core.mail import send_mail
from django.conf import settings
from .tasks import send_email_task


@receiver(post_save, sender=Message)
def create_message(sender, created, instance: Message, **kwargs):
    if created:
       send_email_task.delay("Уведомление",
                             f"Уведомляем вас, что появилось новое событие от преподователя",
                             settings.EMAIL_HOST_USER,
                             [instance.parent.user.email])






