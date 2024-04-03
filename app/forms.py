from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Student, Parent, Teacher, SchoolGroup

class StudentRegisterForm(UserCreationForm):
    school_group = forms.ModelChoiceField(queryset=SchoolGroup.objects.all(), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number', 'school_group')

class ParentRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number')

class TeacherRegisterForm(UserCreationForm):
    prof_of_subject = forms.CharField(max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number', )