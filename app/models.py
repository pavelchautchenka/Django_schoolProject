import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=150, null=False, blank=False)
    phone_number = models.CharField(max_length=100, unique=True, verbose_name="Номер телефона")
    is_active = models.BooleanField(default=False)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True,
                                              verbose_name='user permissions'
                                              )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    parent = models.OneToOneField('Parent', on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    school_group = models.ForeignKey('SchoolGroup', on_delete=models.DO_NOTHING, null=False, blank=True,
                                     related_name="students")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'students'


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'parents'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='teacher_profile', null=True,
                                blank=True)
    my_subject = models.ForeignKey('Subject', on_delete=models.DO_NOTHING, null=True, blank=True, unique=False,
                                   related_name="teachers")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'teachers'


class SchoolGroup(models.Model):
    number = models.IntegerField(null=False, blank=True)


    class Meta:
        db_table = 'school_groups'


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subjects'


class News(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news'


class Grades(models.Model):
    grade = models.IntegerField(null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', null=True)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name='grades', null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, null=True, related_name='grades')

    class Meta:
        db_table = 'grades'

    def __str__(self):
        return self.grade


class Exam(models.Model):
    name = models.CharField(max_length=100, null=False)
    date = models.DateField()
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, related_name="exams", on_delete=models.DO_NOTHING
                                , null=True,blank=True)
    school_group = models.ForeignKey(SchoolGroup, related_name="exams", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'exams'


class Lessons(models.Model):
    subject = models.ForeignKey("Subject", on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)
    date = models.DateTimeField(default=None)
    group = models.ForeignKey("SchoolGroup", on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'lessons'


class HomeWork(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    description = models.TextField()
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True)
    date_creation = models.DateField(default=timezone.now)
    date_deadline = models.DateField(default=None)
    group = models.ManyToManyField(SchoolGroup)

    class Meta:
        db_table = 'homeworks'


class Photo(models.Model):
    title = models.CharField(max_length=100, )
    image = models.ImageField(upload_to='media/', )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "photos"


class Message(models.Model):
    content = models.TextField(null=True)
    parent = models.ForeignKey("Parent", on_delete=models.DO_NOTHING, null=True)
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True)
    date_creation = models.DateField(default=timezone.now)

    class Meta:
        db_table = "messages"
