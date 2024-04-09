from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Message
from django.conf import settings


@shared_task(ignore_result=True, routing_key='email.send')
def send_email_task(subject, message, from_email, recipient_list):
    return send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_event_reminders():
    current_time = timezone.now()
    one_day = current_time + timedelta(days=1)
    six_hours = current_time + timedelta(hours=6)

    events_one_day = Event.objects.filter(meeting_time=one_day)
    events_six_hours = Event.objects.filter(meeting_time=six_hours)

    for event in events_one_day:
        for user in event.users.all():
            send_email_task.delay("Уведомление",
                                  f"Уведомляем вас, что вы согласились посетить {event.name} \n, {event.description} \n,"
                                  f"Мероприятие  проходит завтра  в {event.meeting_time}", settings.EMAIL_HOST_USER,
                                  [user.email], )

    for event in events_six_hours:
        for user in event.users.all():
            send_email_task.delay("Уведомление",
                                  f"Уведомляем вас, что вы согласились посетить {event.name} \n, {event.description} \n,"
                                  f"Мероприятие  проходит сегодня  в {event.meeting_time}", settings.EMAIL_HOST_USER,
                                  [user.email], )
