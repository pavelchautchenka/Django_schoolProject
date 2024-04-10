from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.models import News, Student, Parent, Teacher, Grades, Exam, HomeWork, Lessons, Message


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['subject', 'description', 'date', 'group']


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = ['subject', 'description', 'date_creation', 'date_deadline', 'group']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'description', 'date']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'description', 'teacher', 'school_group']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("user", "my_subject")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = ['grade', 'subject', 'teacher']


class StudentSerializer(serializers.ModelSerializer):
    grades = GradeSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'school_group', 'grades']


class ParentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Parent
        fields = ("id", "user", 'student')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'parent', 'teacher', 'date_creation']