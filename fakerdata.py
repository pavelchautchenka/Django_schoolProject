import sys
import os
from datetime import datetime
from django.utils import timezone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School.settings')
from faker import Faker
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School.settings')
from django import setup
import random

setup()
from app.models import News, Exam, User, Student, Parent, Teacher, Subject, SchoolGroup, Message ,Grades,Lessons, HomeWork

fake = Faker('ru')

subject_names = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Art', 'Music',
                 'Physical Education', 'English']


def create_subject():
    for name in subject_names:
        Subject.objects.get_or_create(name=name)


def create_school_groups():
    numbers_of_groups = [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44, 51, 52, 53, 54, 61, 62, 63, 64]

    for _ in numbers_of_groups:
        SchoolGroup.objects.create(number=_)


def create_fake_news(limit):
    for i in range(limit):
        title = fake.sentence(nb_words=5)
        description = fake.text()
        date = fake.date()
        News.objects.create(title=title, description=description, date=date)


def create_student_and_parent(n):
    for _ in range(n):
        student_first_name = fake.first_name()
        student_last_name = fake.last_name()
        parent_first_name = fake.first_name()
        parent_last_name = fake.last_name()

        student_user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            first_name=student_first_name,
            last_name=student_last_name,
            phone_number=fake.phone_number(),
            password='123'
        )

        parent_user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            first_name=parent_first_name,
            last_name=parent_last_name,
            phone_number=fake.phone_number(),
            password='123'
        )

        student = Student.objects.create(
            user=student_user,
            school_group=random.choice(SchoolGroup.objects.all())
        )

        parent = Parent.objects.create(
            user=parent_user
        )

        student.parent = parent
        student.save()


def create_teachers(n):
    subjects = list(Subject.objects.all())

    for _ in range(n):
        teacher_first_name = fake.first_name()
        teacher_last_name = fake.last_name()

        teacher_user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            first_name=teacher_first_name,
            last_name=teacher_last_name,
            phone_number=fake.phone_number(),
            password='123'
        )

        teacher = Teacher.objects.create(
            user=teacher_user,
            my_subject=random.choice(subjects)
        )


def create_fake_messages(n):
    parents = list(Parent.objects.all())
    teachers = list(Teacher.objects.all())

    for _ in range(n):
        content = fake.paragraph()
        parent = random.choice(parents) if parents else None
        teacher = random.choice(teachers) if teachers else None

        Message.objects.create(
            content=content,
            parent=parent,
            teacher=teacher
        )

def create_fake_grades():
    students = Student.objects.all()
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    for student in students:
        for _ in range(10):
            grade = Grades(
                student=student,
                subject=random.choice(subjects),
                grade=random.randint(1, 5) ,
                teacher=random.choice(teachers)
            )
            grade.save()

def create_exams():
    teachers = Teacher.objects.all()
    school_groups = SchoolGroup.objects.all()
    subjects = Subject.objects.all()

    for _ in range(100):
        Exam.objects.create(
            name=fake.word(),
            date=fake.date(),
            description=fake.text(),
            teacher=random.choice(teachers),
            school_group=random.choice(school_groups)
        )

def create_homeworks():
    teachers = Teacher.objects.all()
    school_groups = SchoolGroup.objects.all()
    subjects = Subject.objects.all()

    for _ in range(10):
        homework = HomeWork.objects.create(
            subject=random.choice(subjects),
            description=fake.text(),
            teacher=random.choice(teachers),
            date_creation=fake.date(),
            date_deadline=fake.date_between(start_date="today", end_date="+30d")
        )

        selected_groups = random.sample(list(school_groups), k=random.randint(1, len(school_groups)))
        homework.group.set(selected_groups)

def create_schedule_lessons():
    teachers = Teacher.objects.all()
    school_groups = SchoolGroup.objects.all()
    subjects = Subject.objects.all()

    for _ in range(200):
        naive_datetime = fake.date_time_this_month()
        aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())

        Lessons.objects.create(
                subject=random.choice(subjects),
                description=fake.text(),
                date=aware_datetime,
                group=random.choice(school_groups)
            )


if __name__ == '__main__':
     create_fake_news(100)
     create_subject()
     create_school_groups()
     create_fake_news(100)
     create_fake_messages(500)

    # create_student_and_parent(500)
    # create_teachers(30)
    # create_fake_grades()
    # create_homeworks()
    #
    #
     #create_exams()
    #
    # create_schedule_lessons()


