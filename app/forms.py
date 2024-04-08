from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Student, Parent, Teacher, SchoolGroup, Subject
from django_select2.forms import Select2MultipleWidget




class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    phone_number = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number')


class StudentRegisterForm(UserCreationForm):
    school_group = forms.ModelChoiceField(queryset=SchoolGroup.objects.all(), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number', 'school_group')


class ParentRegisterForm(UserCreationForm):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), required=False, widget=forms.SelectMultiple)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number','students')


class TeacherRegisterForm(UserCreationForm):
    prof_of_subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=False, widget=forms.SelectMultiple)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number',)
