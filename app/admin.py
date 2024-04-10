from django.contrib import admin
from .models import User, Student, Parent, Teacher, SchoolGroup, Subject, News, Grades, Exam, Lessons, HomeWork, Photo, \
    Message


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 1


class LessonsInLine(admin.TabularInline):
    model = Lessons
    extra = 1


@admin.register(SchoolGroup)
class SchoolGroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline, ExamInline, LessonsInLine]
    list_display = ('number', 'display_students')  # Отображение номера группы и списка учеников
    search_fields = ['number']

    def display_students(self, obj):
        students = obj.students.select_related('user').all()[:10]  # Ограничение количества отображаемых учеников до 10
        return ", ".join([student.user.get_full_name() for student in students])

    display_students.short_description = 'Ученики'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date',)
    search_fields = ('title', 'description', 'date',)


@admin.register(Exam)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name','date','description','teacher','school_group')
    search_fields = ('name','date','description')

@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'description','group')
    search_fields = ('subject', 'date', 'description','group')

@admin.register(Grades)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'student', 'subject', 'teacher')
    search_fields = ('grade', 'student__user__first_name', 'student__user__last_name', 'teacher__user__first_name',
                     'teacher__user__last_name', 'subject__name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'phone_number')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    actions = ['confirm_user']

    @admin.action(description='Confirm User')
    def confirm_user(self, request, queryset):
        queryset.update(is_active=True)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'parent', 'school_group')
    search_fields = ('user__first_name', 'user__last_name')

    def get_student_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    get_student_name.short_description = 'Student Name'


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_parent_name', 'children',)
    search_fields = ('user__first_name', 'user__last_name')

    def get_parent_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    get_parent_name.short_description = 'Parent Name'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_teacher_name', 'my_subject')

    def get_teacher_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    get_teacher_name.short_description = 'Teacher Name'
