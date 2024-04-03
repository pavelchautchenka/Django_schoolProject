from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, ParentRegisterForm, TeacherRegisterForm
from app.models import Student, Teacher, Parent, Grades, ScheduleExams, ScheduleLessons, HomeWork
from app.models import News
from app.services import send_activation_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime


def home_page(request: WSGIRequest):
    queryset = News.objects.order_by("-date")[:10]
    return render(request, 'main/main.html', {"news": queryset})


def register_user(request, user_type):
    form_classes = {
        'student': StudentRegisterForm,
        'parent': ParentRegisterForm,
        'teacher': TeacherRegisterForm
    }
    model_classes = {
        'student': Student,
        'parent': Parent,
        'teacher': Teacher
    }

    if request.method == 'POST':
        form = form_classes[user_type](request.POST)
        if form.is_valid():
            user = form.save()

            if user_type == 'student':
                school_group = form.cleaned_data.get('school_group')
                student = model_classes[user_type].objects.create(user=user, school_group=school_group)
                school_group.students.add(student)
            else:
                model_classes[user_type].objects.create(user=user)
            send_activation_email(user=user, request=request)
            return redirect('home')
    else:
        form = form_classes[user_type]()

    return render(request, 'user/registration.html', {'form': form, 'role': user_type})

def contacts_views(request: WSGIRequest):
    return render(request, 'main/contacts.html')


def info_views(request: WSGIRequest):
    return render(request, 'main/info_for_stud.html')

def gallery_views(request: WSGIRequest):

    return render(request, 'main/gallery.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active == True:
                login(request, user)
                if hasattr(user, 'student_profile'):
                    return redirect('student_diary')  # URL для студента
                elif hasattr(user, 'teacher_profile'):
                    return redirect('teacher_dashboard')  # URL для учителя
                elif hasattr(user, 'parent_profile'):
                    return redirect('parent_dashboard')  # URL для родителя
                else:
                    form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'user/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def student_dashboard(request):
    students = Student.objects.get(user=request.user)
    grades = Grades.objects.filter(student=students)
    return render(request, 'student/diary_grade.html', {"grades": grades})


@login_required
def schedule_exams(request):
    student = Student.objects.get(user=request.user)
    current_date = datetime.now()
    exams = ScheduleExams.objects.filter(school_group=student.school_group, date__gte=current_date)
    return render(request, 'student/exams.html', {"exams": exams})


@login_required
def home_work_views(request):
    current_date = datetime.now()
    students = Student.objects.get(user=request.user)
    homeworks = HomeWork.objects.filter(group=students.school_group, date_deadline__gte=current_date)
    return render(request, 'student/homework_view.html', {"homeworks": homeworks})


from django.db.models import DateField
from django.db.models.functions import Trunc

@login_required
def schedule_lessons_view(request):
    current_date = datetime.now()
    student = Student.objects.get(user=request.user)
    lessons = ScheduleLessons.objects.filter(group=student.school_group, date__gte=current_date)
    lessons = lessons.annotate(date_only=Trunc('date', 'day', output_field=DateField())).order_by('date_only')

    lessons_by_date = {}
    for lesson in lessons:
        lessons_by_date.setdefault(lesson.date_only, []).append(lesson)

    return render(request, 'student/schedule_lessons.html', {'lessons_by_date': lessons_by_date})


@login_required
def parent_dashboard(request):
    parent = Parent.objects.get(user=request.user)
    student = Student.objects.get(parent=parent)

    return render(request, 'parent/parent_main.html', )
