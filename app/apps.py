from django.apps import AppConfig
from django.db.models.signals import post_save


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from .signals import create_message
        from .models import Message
        post_save.connect(create_message, sender=Message)
