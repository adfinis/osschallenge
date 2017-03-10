import base64
import os
from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView
from .models import Task, Project, Profile
from django.contrib.auth.models import User
from .forms import TaskForm, ProjectForm, ProfileForm, UserForm
from django.views.generic import FormView
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.conf import settings


def IndexView(request):
    template_name = 'osschallenge/index.html'

    return render(request, template_name)


class NewProjectView(CreateView):
    model = Project
    template_name = 'osschallenge/newproject.html'
    fields = [
        'title',
        'lead_text',
        'description',
        'licence',
        'github',
        'website',
        'owner'
    ]

    def form_valid(self, form):
        return super(NewProjectView, self).form_valid(form)

    success_url = '/projects/'


class ProjectIndexView(generic.ListView):
    template_name = 'osschallenge/projectindex.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(generic.DetailView):
    model = Project
    template_name = 'osschallenge/project.html'


def EditProjectView(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save()
            return redirect('project', pk=project.pk)

    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        'osschallenge/editproject.html',
        {
            'form': form,
            'project': project,
        }
    )


class TaskIndexView(generic.ListView):
    template_name = 'osschallenge/taskindex.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.all()


class TaskView(generic.DetailView):
    model = Task
    template_name = 'osschallenge/task.html'


def EditTaskView(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()
            return redirect('task', pk=task.pk)

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        'osschallenge/edittask.html',
        {
            'form': form,
            'task': task,
        }
    )


class NewTaskView(CreateView):
    model = Task
    template_name = 'osschallenge/newtask.html'
    fields = [
        'title',
        'lead_text',
        'description',
        'mentor',
    ]

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
        return super(NewTaskView, self).form_valid(form)

    success_url = '/tasks/'


def ProfileView(request):

    if request.user.is_authenticated():
        return render(request, 'osschallenge/profile.html')
    else:
        return redirect('/login/')


def EditProfileView(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        form_profile = ProfileForm(request.POST, instance=profile)
        form_user = UserForm(request.POST, instance=user)

        if form_profile.is_valid() and form_user.is_valid():
            profile = form_profile.save()
            user = form_user.save()
            return redirect('profile')

    else:
        form_profile = ProfileForm(instance=profile)
        form_user = UserForm(instance=user)

    return render(
        request,
        'osschallenge/editprofile.html',
        {
            'form_profile': form_profile,
            'form_user': form_user,
            'profile': profile,
            'user': user,
        }
    )


class RankingView(generic.ListView):
    template_name = 'osschallenge/ranking.html'
    context_object_name = 'ranking_list'

    def get_queryset(self):
        return User.objects.order_by('-profile__points')


def generate_key():
    return base64.b32encode(os.urandom(7))[:10].lower()


class RegistrationView(FormView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/registration_send_mail/'

    def form_valid(self, form):
        user = User.objects.create_user(form.data['username'],
                                        form.data['email'],
                                        form.data['password1'],
                                        first_name=form.data['first_name'],
                                        last_name=form.data['last_name'])
        user.is_active = False
        user.save()

        if user is not None:
            self.generate_profile(user)

        return super(RegistrationView, self).form_valid(form)

    def generate_key():
        return base64.b32encode(os.urandom(7))[:10].lower()

    def generate_profile(self, user):
        profile = Profile(key=generate_key(), user=user)
        profile.save()
        send_mail(
            'OSS-Challenge account confirmation',
            """
            Hello,

            please click this link to activate your OSS-Challenge account:
            {}/registration_done/{}

            Sincerely,
            The OSS-Challenge Team
            """.format(settings.SITE_URL, profile.key),
            'osschallenge@osschallenge.com',
            [user.email],
            fail_silently=False,
        )


class RegistrationDoneView(generic.TemplateView):
    template_name = 'osschallenge/registration_done.html'

    def get_context_data(request, key):
            matches = Profile.objects.filter(key=key)
            if matches.exists():
                profile = matches.first()
                if profile.user.is_active:
                    request.template_name = 'osschallenge/user_is_already_active.html'
                else:
                    profile.user.is_active = True
                    profile.user.save()
            else:
                request.template_name = 'osschallenge/registration_failed.html'


class RegistrationSendMailView(generic.TemplateView):
    template_name = 'osschallenge/registration_send_mail.html'
