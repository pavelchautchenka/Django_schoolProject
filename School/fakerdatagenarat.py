
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School.settings')
from faker import Faker
from django.contrib.auth.hashers import make_password
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School.settings')
from django import setup
setup()
from app.models import News,ScheduleExams

faker = Faker('ru')

def create_fake_news(limit):
    for i in range(limit):
        title = faker.sentence(nb_words=5)
        description = faker.text()
        date = faker.date()
        News.objects.create(title=title, description=description, date=date)




def create_fake_exams(limit):
    for i in range(limit):
        name = faker.sentence(nb_words=5)
        date = faker.date()
        description = faker.text()
        ScheduleExams.objects.create(name=name, date=date, description=description)

if __name__ == '__main__':
     create_fake_exams(50)