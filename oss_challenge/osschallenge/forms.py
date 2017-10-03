from django import forms
from django.forms import ModelForm, Textarea
from .models import Task, Project, Profile, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django_markdown.fields import MarkdownFormField


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')


class RegistrationForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=30)
    first_name = forms.CharField(label=_('First name'), max_length=30)
    last_name = forms.CharField(label=_('Last name'), max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('Password (Again)'),
                                widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Passwords do not match.')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email is already taken.')


class MentorForm(forms.Form):
    assign_mentor = forms.CharField(label='New mentor')


class CommentForm(ModelForm):
    comment = MarkdownFormField()

    class Meta:
        model = Comment
        fields = ['comment']


class TaskForm(ModelForm):
    picture = forms.ImageField(label=_('Add picture'), required = False, widget=forms.FileInput)

    class Meta:
        model = Task
        fields = [
            'title_de',
            'title_en_us',
            'lead_text_de',
            'lead_text_en_us',
            'description_de',
            'description_en_us',
            'picture'
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


class ProjectForm(ModelForm):
    mentors = forms.ModelMultipleChoiceField(label=_('Choose  mentors'), queryset=User.objects.filter(profile__role_id=2))

    class Meta:
        model = Project
        fields = [
            'title_de',
            'title_en_us',
            'lead_text_de',
            'lead_text_en_us',
            'description_de',
            'description_en_us',
            'licence',
            'github',
            'website',
            'mentors'
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


class ProfileForm(ModelForm):
    picture = forms.ImageField(label=_('Change picture'), required = False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = [
            'links',
            'contact',
            'picture'
        ]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
