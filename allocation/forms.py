from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

DEPARTMENT_CHOICES = [
    ('CSE', 'Computer Science Engineering'),
    ('ECE', 'Electronics and Communication Engineering'),
    ('ME', 'Mechanical Engineering'),
]

class CreateUserForm(UserCreationForm):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=True, label='Department')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'department']