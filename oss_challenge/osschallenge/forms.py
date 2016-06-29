from django import forms
from django.forms import ModelForm
from .models import Task


class MentorForm(forms.Form):
    assign_mentor = forms.CharField(label='New mentor')


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'lead_text', 'description', 'mentor']
