from django import forms
from django.forms import ModelForm
from .models import Task


class MentorForm(forms.Form):
    assign_mentor = forms.CharField(label='New mentor')


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'lead_text', 'description', 'mentor']

form = TaskForm()

# title = forms.CharField(max_length=50)
# lead_text = forms.CharField(widget=forms.Textarea, max_length=300)
# description = forms.CharField(widget=forms.Textarea)
# mentor = forms.CharField()
