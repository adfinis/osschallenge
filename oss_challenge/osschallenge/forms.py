from django import forms
from django.forms import ModelForm, Textarea
from .models import Task, Project, User


class MentorForm(forms.Form):
    assign_mentor = forms.CharField(label='New mentor')


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'lead_text', 'description', 'mentor']
        widgets = {
            
            'lead_text': Textarea(attrs={
                'cols': 100, 
                'rows': 3,
            }),
            
            'description': Textarea(attrs={
                'cols': 100,
                'rows': 8,
            }),
        
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'lead_text',
            'description',
            'licence',
            'github',
            'website',
            'owner'
        ]
        widgets = {
            'lead_text': Textarea(attrs={
                'cols': 100,
                'rows': 3,
            }),
            
            'description': Textarea(attrs={
                'cols': 100,
                'rows': 8,
            }),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname',
            'surname',
            'lastname',
            'mail',
        ]
