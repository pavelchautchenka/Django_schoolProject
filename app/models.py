import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=150, null=False, blank=False)
    phone_number = models.CharField(max_length=100, unique=True, verbose_name="Номер телефона")
    is_active = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group,related_name='custom_user_groups',blank=True,verbose_name='groups')
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_permissions',blank=True,verbose_name='user permissions'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile',null=True,blank=True)
    parent = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    school_group = models.ForeignKey('SchoolGroup', on_delete=models.CASCADE, null=True, blank=True, related_name="students")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'students'


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile',null=True, blank=True)
    students = models.ManyToManyField('Student', related_name="parents")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'parents'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='teacher_profile',null=True, blank=True)
    prof_of_subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'teachers'

class SchoolGroup(models.Model):
    name = models.CharField(max_length=10, unique=True)
    student = models.ManyToManyField("Student", related_name="group_students")
    teacher = models.ManyToManyField("Teacher")
    subject = models.ManyToManyField("Subject")
    #
    def __str__(self):
        return self.name

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
    grade = models.IntegerField( null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher , on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.grade

class ScheduleExams(models.Model):
    name = models.CharField(max_length=100, null=False)
    date = models.DateField()
    description = models.TextField()
    teacher = models.ManyToManyField("Teacher", related_name="subject_teachers",null=True, blank=True)
    subject = models.ForeignKey("Subject", on_delete=models.DO_NOTHING,null=True, blank=True)
    school_group = models.ManyToManyField(SchoolGroup,)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'exams'

class ScheduleLessons(models.Model):
    subject = models.ForeignKey("Subject", on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)
    date = models.DateTimeField(default=None)
    teacher = models.ManyToManyField("Teacher")
    group = models.ForeignKey("SchoolGroup", on_delete=models.DO_NOTHING, null=True)


    class Meta:
        db_table = 'lessons'


class HomeWork(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    description = models.TextField()
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True)
    date_creation = models.DateField(default=datetime.now())
    date_deadline = models.DateField(default=None)
    group = models.ManyToManyField(SchoolGroup)


from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=100,)
    image = models.ImageField(upload_to='media/',)


    def __str__(self):
        return self.title

    class Meta:
        db_table  = "photo"


class Message(models.Model):
    content = models.TextField(null=True)
    parent = models.ForeignKey("Parent", on_delete=models.DO_NOTHING, null=True)

    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True)
    date_creation = models.DateField(default=datetime.now())

    class Meta:
        db_table = "messages"





