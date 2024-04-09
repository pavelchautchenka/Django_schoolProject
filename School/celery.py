import os
from celery import Celery
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School.settings')
app = Celery('app') # or app
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('default', routing_key='task.#'),
    Queue('email_queue', routing_key='email.#'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'topic'
app.conf.task_default_routing_key = 'task.#'
