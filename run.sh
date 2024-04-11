#!/bin/sh
chmod +x ./manage.py
python manage.py createsuperuser --noinput;
python manage.py makemigrations;
python manage.py migrate;
gunicorn -w 2 -b 0.0.0.0:8000 School.wsgi:application;