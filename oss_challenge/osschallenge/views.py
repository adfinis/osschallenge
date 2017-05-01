import base64
import os
from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.generic.edit import CreateView
from .models import Task, Project, Profile, Comment
from django.contrib.auth.models import User
from .forms import TaskForm, ProjectForm, ProfileForm, UserForm, CommentForm
from django.views.generic import FormView
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

CONTRIBUTOR_ID = 1
MENTOR_ID = 2


def IndexView(request):
    template_name = 'osschallenge/index.html'

    return render(request, template_name, {
        'mentor_id': MENTOR_ID
    })


class NewProjectView(CreateView):
    model = Project
    template_name = 'osschallenge/newproject.html'
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
        'owner'
    ]

    def form_valid(self, form):
        return super(NewProjectView, self).form_valid(form)

    success_url = '/projects/'


def ProjectIndexView(request):
    project_list = get_list_or_404(Project)
    template_name = 'osschallenge/projectindex.html'
    return render(request, template_name, {
        'project_list': project_list,
        'mentor_id': MENTOR_ID
    })


def ProjectView(request, pk):
    project = get_object_or_404(Project, pk=pk)
    template_name = 'osschallenge/project.html'
    return render(request, template_name, {
        'project': project,
        'mentor_id': MENTOR_ID
    })


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


def TaskIndexView(request):
    task_list = get_list_or_404(Task)
    template_name = 'osschallenge/taskindex.html'
    return render(request, template_name, {
        'task_list': task_list,
        'mentor_id': MENTOR_ID
    })


def TaskView(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = get_object_or_404(User, pk=request.user.id)
    template_name = 'osschallenge/task.html'
    if 'Claim' in request.POST:
        task.assignee_id = user.id
        task.save()

    elif 'Release' in request.POST:
        task.assignee_id = None
        task.save()

    elif 'Task done' in request.POST:
        task.task_done = True
        task.assignee_id = user.id
        task.save()

    elif 'Comment' in request.POST:
        comment = Comment()
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment.author = user
            comment.task = task
            comment = form.save()

    return render(request, template_name, {
        'comment_list': sorted(get_list_or_404(Comment), key=lambda c: c.created_at, reverse=True),
        'task': task,
        'user': user,
        'mentor_id': MENTOR_ID
    })


def EditTaskView(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)

        print(form.is_valid())
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


def NewTaskView(request, pk):
    task = Task()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)

        print(form.is_valid())
        if form.is_valid():
            form.instance.project = Project.objects.get(pk=pk)
            task = form.save()
            return redirect('task', pk=task.pk)

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        'osschallenge/newtask.html',
        {
            'form': form,
            'task': task,
        }
    )


def ProfileView(request):
    finished_tasks_list = get_list_or_404(Task)
    user_profile_points = 0
    template_name = 'osschallenge/profile.html'

    if request.user.is_authenticated():
        return render(request, template_name, {
            'contributor_id': CONTRIBUTOR_ID,
            'mentor_id': MENTOR_ID,
            'finished_tasks_list': finished_tasks_list,
            'user_profile_points': user_profile_points
        })
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


def TaskAdministrationIndexView(request):
    finished_task_list = get_list_or_404(Task)
    template_name = 'osschallenge/task_administration_index.html'

    if request.user.is_authenticated():
        return render(request, template_name, {
            'finished_task_list': finished_task_list,
            'contributor_id': CONTRIBUTOR_ID,
            'mentor_id': MENTOR_ID
        })


def TaskAdministrationView(request, pk):
    task = get_object_or_404(Task, pk=pk)
    profile = get_object_or_404(Profile, user_id=task.assignee_id)
    user = get_object_or_404(User, pk=request.user.id)
    finished_task_list = get_list_or_404(Task)
    user_profile_points = 0
    template_name = 'osschallenge/task_administration.html'

    if 'Checked' in request.POST:
        task.task_checked = True
        profile.points += 5
        task.save()
        profile.save()

    if 'Reopen' in request.POST:
        task.task_checked = False
        profile.points -= 5
        task.save()
        profile.save()

    if request.user.is_authenticated():
        return render(request, template_name, {
            'finished_task_list': finished_task_list,
            'mentor_id': MENTOR_ID,
            'contributor_id': CONTRIBUTOR_ID,
            'task': task,
            'user': user,
            'profile': profile,
            'user_profile_points': user_profile_points
        })


def RankingView(request):
    ranking_list = User.objects.order_by('-profile__points')
    template_name = 'osschallenge/ranking.html'
    return render(request, template_name, {
        'ranking_list': ranking_list,
        'mentor_id': MENTOR_ID,
    })


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
        profile = Profile(key=self.generate_key(), user=user)
        profile.save()
        send_mail(
            _('OSS-Challenge account confirmation'),
            _("""
            Hello,

            please click this link to activate your OSS-Challenge account:
            {}/registration_done/{}

            Sincerely,
            The OSS-Challenge Team
            """).format(settings.SITE_URL, profile.key),
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
