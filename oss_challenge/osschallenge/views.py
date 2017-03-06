import base64
import os
from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView
from .models import Task, Project, Account, UserProfile
from django.contrib.auth.models import User
from .forms import TaskForm, ProjectForm
from django.views.generic import FormView
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.conf import settings


def IndexView(request):
    template_name = 'osschallenge/index.html'

    return render(request, template_name)


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
            self.generate_account(user)

        return super(RegistrationView, self).form_valid(form)

    def generate_account(self, user):
        account = Account(key=generate_key())
        account.save()
        user_profile = UserProfile(
            user=user,
            account=account
        )
        user_profile.save()
        send_mail(
            'OSS-Challenge account confirmation',
            """
            Hello,

            please click this link to activate your OSS-Challenge account:
            {}/registration_done/{}

            Sincerely,
            The OSS-Challenge Team
            """.format(settings.SITE_URL, account.key),
            'osschallenge@osschallenge.ml',
            [user.email],
            fail_silently=False,
        )


class RegistrationDoneView(generic.TemplateView):
    template_name = 'osschallenge/registration_done.html'

    def get_context_data(request, key):
            matches = Account.objects.filter(key=key)
            if matches.exists():
                account = matches.first()
                user_profile = UserProfile.objects.get(account=account)
                if user_profile.user.is_active:
                    request.template_name = 'osschallenge/user_is_already_active.html'
                else:
                    user_profile.user.is_active = True
                    user_profile.user.save()
            else:
                request.template_name = 'osschallenge/registration_failed.html'


class RegistrationSendMailView(generic.TemplateView):
    template_name = 'osschallenge/registration_send_mail.html'
