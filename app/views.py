from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, ParentRegisterForm, TeacherRegisterForm
from app.models import Student, Teacher, Parent, Grades, Exam, Lessons, HomeWork, Message, Subject, SchoolGroup
from app.models import News
from app.services import send_activation_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
from django.contrib import messages


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
            elif user_type == 'parent':
                parent = model_classes[user_type].objects.create(user=user)
                # Добавление детей к родителю
                for student in form.cleaned_data.get('students', []):
                    parent.students.add(student)
                    student.parents.add(parent)
                    student.save()
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
    student = Student.objects.get(user=request.user)
    grades = Grades.objects.filter(student=student)
    return render(request, 'student/diary_grade.html', {"grades": grades, "student": student})


@login_required
def schedule_exams(request):
    student = Student.objects.get(user=request.user)
    current_date = datetime.now()
    exams = Exam.objects.filter(school_group=student.school_group)
    return render(request, 'student/exams.html', {"exams": exams})


@login_required
def home_work_views(request):
    current_date = datetime.now()
    students = Student.objects.get(user=request.user)
    homeworks = HomeWork.objects.filter(group=students.school_group, date_deadline__gte=current_date)
    return render(request, 'student/homework_view.html', {"homeworks": homeworks})



@login_required
def schedule_lessons_view(request):
    student = Student.objects.get(user=request.user)
    lessons = Lessons.objects.filter(group=student.school_group)
    return render(request, 'student/schedule_lessons.html', {'lessons': lessons})


@login_required
def parent_dashboard(request):
    parent = Parent.objects.get(user=request.user)
    student = Student.objects.filter(parent=parent).first()

    grades = Grades.objects.filter(student=student)
    return render(request, 'parent/parent_grade.html', {"student": student, "grades": grades})


@login_required
def parent_message(request):
    parent = Parent.objects.get(user=request.user)
    student = Student.objects.filter(parent=parent).first()
    parent_messages = Message.objects.filter(parent=parent)
    return render(request, 'parent/parent_message.html', {"parent_messages": parent_messages, "student": student})


@login_required
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect('parent_message')


@login_required
def parent_home_work_views(request):
    current_date = datetime.now()
    parent = Parent.objects.get(user=request.user)
    student = Student.objects.filter(parent=parent).first()

    homeworks = HomeWork.objects.filter(group=student.school_group, date_deadline__gte=current_date)
    return render(request, 'parent/parent_homework.html', {"homeworks": homeworks, "student": student})


@login_required
def parent_schedule_views(request):
    current_date = datetime.now()
    parent = Parent.objects.get(user=request.user)
    student = Student.objects.filter(parent=parent).first()


    exams = Exam.objects.filter( date__gte=current_date,school_group=student.school_group)
    return render(request, 'parent/parent_schedule.html', {"exams": exams, "student": student, })


@login_required
def teacher_dashboard(request):
    return render(request,'teacher/teacher_main.html',{"user": request.user})

@login_required
def teacher_send_message(request):
    if request.method == 'POST':
        parent_id = request.POST.get('parent')
        message_text = request.POST.get('message')
        parent = Parent.objects.get(id=parent_id)
        Message.objects.create(
            content=message_text,
            date_creation=datetime.now(),
            parent=parent,
            teacher=Teacher.objects.get(user=request.user)
        )
        messages.success(request, "Ваше сообщение отправлено")
        return redirect('teacher_dashboard',)

    parents = Parent.objects.all()
    return render(request, 'teacher/teacher_send_message.html', {'parents': parents})

@login_required
def teacher_post_grade(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        grade_value = request.POST.get('grade')
        student = Student.objects.get(id=student_id)

        # Создаем и сохраняем оценку
        Grades.objects.create(
            student=student,
            grade=grade_value,
            # Указываем учителя, выставляющего оценку
            teacher=request.user.teacher_profile
        )

        # Перенаправление после отправки формы
        return redirect('teacher_post_grade')

        # Для GET запроса предоставляем список учеников
    students = Student.objects.all()
    return render(request, 'teacher/teacher_post_grades.html', {'students': students})

@login_required
def teacher_create_hw(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        description = request.POST.get('description')
        date_deadline = request.POST.get('date_deadline')
        subject = Subject.objects.get(id=subject_id)
        school_group = SchoolGroup.objects.all()

        HomeWork.objects.create(
            subject=subject,
            description=description,

            date_deadline= date_deadline,
            group = school_group[0]
        )

        return redirect('some_view')

    subjects = Subject.objects.all()
    return render(request, 'teacher/teacher_create_homework.html', {'subjects': subjects})

# TODO: доделать тут список групп при выдачи ДЗ