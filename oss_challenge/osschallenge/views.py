import base64
import os
import time
import bisect
from django.views import generic
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from .models import Task, Project, Profile, Comment, Rank
from django.contrib.auth.models import User
from .forms import TaskForm, ProjectForm, ProfileForm, UserForm, CommentForm
from django.views.generic import FormView
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count, Case, When
from datetime import datetime

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
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewProjectView, self).form_valid(form)

    success_url = '/projects/'


def ProjectIndexView(request):
    project_list = list(Project.objects.all())
    template_name = 'osschallenge/projectindex.html'
    return render(request, template_name, {
        'project_list': project_list,
        'mentor_id': MENTOR_ID
    })


def ProjectView(request, pk):
    project = Project.objects.get(pk=pk)
    task_objects = Task.objects.filter(project_id=project.id)
    task_list = []
    max_length_description = 130
    max_length_title = 60
    for obj in task_objects:
        task_list.append(obj)
    for task in task_objects:
        task.description = shorten(task.description, max_length_description)
        task.title = shorten(task.title, max_length_title)
    mentors = project.mentors.all()
    owner = project.owner
    current_user_id = request.user.id
    can_create_new_tasks = project.mentors.filter(id=current_user_id)
    template_name = 'osschallenge/project.html'

    return render(request, template_name, {
        'project': project,
        'mentor_id': MENTOR_ID,
        'mentors' : mentors,
        'owner' : owner,
        'current_user_id': current_user_id,
        'can_create_new_tasks': can_create_new_tasks,
        'task_list': task_list
    })


def EditProjectView(request, pk):
    project = Project.objects.get(pk=pk)

    if 'delete-project' in request.POST:
        project.delete()
        return redirect('/projects/')

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


def MyTaskIndexView(request, username):
    max_length_description = 130
    max_length_title = 60
    template_name = 'osschallenge/mytasksindex.html'
    current_user_id = request.user.id
    user_task_objects = Task.objects.filter(assignee_id=current_user_id)
    user_task_list = []
    for obj in user_task_objects:
        user_task_list.append(obj)
    for task in user_task_objects:
        task.description = shorten(task.description, max_length_description)
        task.title = shorten(task.title, max_length_title)
    if request.GET:
        match_list = Task.objects.filter(
            Q(title__icontains=request.GET['search']) |
            Q(project__title__icontains=request.GET['search'])).distinct()
        if match_list:
            for match in match_list:
                match.description = shorten(
                    match.description, max_length_description
                )
                match.title = shorten(match.title, max_length_title)
            return render(request, template_name, {
                'match_list': match_list,
                'user_task_list': user_task_list
            })
        else:
            return render(request, template_name, {
                'user_task_list': user_task_list,
                'match_list': match_list,
            })
    return render(request, template_name, {
        'user_task_list': user_task_list,
        'mentor_id': MENTOR_ID
    })


def shorten(string, max_length):
    if len(string) > max_length:
        return string[:max_length] + " ..."
    return string


def TaskIndexView(request):
    task_list = list(Task.objects.all())
    template_name = 'osschallenge/taskindex.html'
    max_length_description = 130
    max_length_title = 60
    no_tasks = "There are no tasks"
    for task in task_list:
        task.description = shorten(task.description, max_length_description)
        task.title = shorten(task.title, max_length_title)
    if request.GET:
        match_list = Task.objects.filter(
            Q(title__icontains=request.GET['search']) |
            Q(project__title__icontains=request.GET['search'])).distinct()
        if match_list:
            for match in match_list:
                match.description = shorten(
                    match.description, max_length_description
                )
                match.title = shorten(match.title, max_length_title)
            return render(request, template_name, {
                'match_list': match_list,
                'task_list': task_list
            })
        else:
            return render(request, template_name, {
                'no_tasks': no_tasks,
                'task_list': task_list,
                'match_list': match_list,
            })
    return render(request, template_name, {
        'task_list': task_list,
        'mentor_id': MENTOR_ID
    })


def TaskView(request, pk):
    task = Task.objects.get(pk=pk)
    template_name = 'osschallenge/task.html'
    notification = ""
    render_params = {}
    # import ipdb; ipdb.set_trace()
    if request.user.id:
        user = request.user
        project = Project.objects.get(pk=task.project_id)
        render_params['user'] = User.objects.get(pk=request.user.id)
        render_params['mentor_id'] = MENTOR_ID
        render_params['contributor_id'] = CONTRIBUTOR_ID
        render_params['mentors'] = project.mentors.all()
        render_params['is_mentor_of_this_task'] = project.mentors.filter(
            id=user.id
        )

        if 'Claim' in request.POST:
            task.assignee_id = user.id
            task.save()

        elif 'Release' in request.POST:
            task.assignee_id = None
            task.task_done = False
            task.save()

        elif 'Task done' in request.POST:
            task.task_done = True
            task.assignee_id = user.id
            task.save()

        elif 'Comment' in request.POST:
            comment = Comment()
            form = CommentForm(request.POST, instance=comment)
            notification = _("Your comment has been posted")
            render_params['notification'] = notification
            if form.is_valid():
                comment.author = user
                comment.task = task
                comment = form.save()

        elif 'Delete-comment' in request.POST:
            comment_id = (request.POST['Delete-comment'])
            comment = Comment.objects.get(pk=comment_id)
            if comment.author_id == request.user.id:
                comment.delete()

        elif 'Approve' in request.POST:
            profile = Profile.objects.get(user_id=task.assignee_id)
            task.task_checked = True
            task.approved_by = user
            task.approval_date = timezone.localtime(timezone.now())
            task.save()
            profile.save()

        elif 'Reopen' in request.POST:
            profile = Profile.objects.get(user_id=task.assignee_id)
            task.task_checked = False
            task.approval_date = None
            task.save()
            profile.save()

    render_params['comment_list'] = sorted(Comment.objects.all(),
                                           key=lambda c: c.created_at)
    render_params['task'] = task
    return render(request, template_name, render_params)


def EditTaskView(request, pk):
    task = Task.objects.get(pk=pk)
    user = request.user
    project = Project.objects.get(pk=task.project_id)
    is_mentor_of_this_task = project.mentors.filter(id=user.id)

    if 'Delete-task' in request.POST:
        task.delete()
        return redirect('/tasks/')

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)

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
            'is_mentor_of_this_task': is_mentor_of_this_task
        }
    )


def NewTaskView(request, pk):
    task = Task()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)

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


def ProfileView(request, username):
    user = User.objects.get(username=username)
    max_length_description = 130
    max_length_title = 60
    template_name = 'osschallenge/profile.html'
    approved_tasks = Task.objects.filter(
        Q(task_checked=True) &
        Q(assignee_id=user.id)
    ).count()
    total_points = approved_tasks * 5
    matches = Rank.objects.filter(
        required_points__lte=total_points
    ).order_by('-required_points')
    rank = matches.first()
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        return render(request, 'osschallenge/no_profile_available.html')
    finished_tasks = Task.objects.filter(task_done=True)
    finished_task_list = []
    for obj in finished_tasks:
        finished_task_list.append(obj)
    for task in finished_task_list:
        task.description = shorten(task.description, max_length_description)
        task.title = shorten(task.title, max_length_title)

    if user.is_active is False:
        return render(request, 'osschallenge/profile_does_not_exist.html')

    return render(request, template_name, {
        'contributor_id': CONTRIBUTOR_ID,
        'mentor_id': MENTOR_ID,
        'finished_task_list': finished_task_list,
        'profile': profile,
        'user': user,
        'total_points': total_points,
        'rank': rank,
    })


def ProfileDoesNotExistView(request):
    template_name = 'osschallenge/profile_does_not_exist.html'
    return render(request, template_name, {
    })


def EditProfileView(request):
    user = request.user
    profile = Profile.objects.get(user_id=user.id)

    if 'delete-profile' in request.POST:
        user.is_active = False
        user.profile.links = ""
        user.profile.contact = ""
        user.profile.picture = "static/osschallenge/example.jpg"
        user.save()
        user.profile.save()
        return redirect('/login/')

    if request.method == 'POST':
        form_profile = ProfileForm(
            request.POST, request.FILES, instance=profile
        )
        form_user = UserForm(request.POST, instance=user)

        if form_profile.is_valid() and form_user.is_valid():
            profile = form_profile.save()
            user = form_user.save()
            return redirect('profile', user.username)

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
    user = request.user
    template_name = 'osschallenge/task_administration_index.html'
    max_length_description = 130
    max_length_title = 60
    finished_tasks = Task.objects.filter(task_done=True)
    finished_task_list = []
    for obj in finished_tasks:
        finished_task_list.append(obj)
    for task in finished_task_list:
        task.description = shorten(task.description, max_length_description)
        task.title = shorten(task.title, max_length_title)
    if request.GET:
        match_list = Task.objects.filter(
            Q(title__icontains=request.GET['search']) |
            Q(project__title__icontains=request.GET['search'])
        ).distinct()
        if match_list:
            for match in match_list:
                match.description = shorten(
                    match.description, max_length_description
                )
                match.title = shorten(match.title, max_length_title)
            return render(request, template_name, {
                'match_list': match_list,
                'finished_task_list': finished_task_list
            })
        else:
            return render(request, template_name, {
                'finished_task_list': finished_task_list,
                'match_list': match_list,
            })
    return render(request, template_name, {
        'finished_task_list': finished_task_list,
        'mentor_id': MENTOR_ID,
        'task_list': Task.objects.filter(
            Q(project__mentors__id=user.id) &
            Q(task_done=True)
        )
    })


def RankingView(request):
    quarters = range(1, 12, 3)
    month = int(time.strftime("%m"))
    quarter = bisect.bisect(quarters, month)
    quarter_month = get_quarter_months(str(quarter))
    today = datetime.today()
    quarter_start = [today.year, quarters[quarter - 1], 1]
    if quarter == 4:
        next_quarter = [today.year + 1, 1, 1]
    else:
        next_quarter = [today.year, quarters[quarter], 1]
    contributors = User.objects.filter(profile__role_id=CONTRIBUTOR_ID)
    # for every finished task add 5 points
    contributors_with_points = contributors.annotate(
        task_count=Count(
            Case(
                When(
                    assignee_tasks__task_checked=True
                    , then=1)
            )
        ) * 5, quarter_count=Count(
            Case
            (
                When(
                    Q(assignee_tasks__task_checked=True) &
                    Q(assignee_tasks__approval_date__lt=datetime(
                        next_quarter[0], next_quarter[1], next_quarter[2])
                      ) &
                    Q(assignee_tasks__approval_date__gte=datetime(
                        quarter_start[0], quarter_start[1], quarter_start[2])
                      )
                    , then=1)
            )
        ) * 5)
    ranking_list = contributors_with_points.order_by('-task_count')

    template_name = 'osschallenge/ranking.html'
    return render(request, template_name, {
        'contributor_id': CONTRIBUTOR_ID,
        'ranking_list': ranking_list,
        'mentor_id': MENTOR_ID,
        'quarter': quarter,
        'quarter_month': quarter_month,
    })


def get_quarter_months(string_of_current_quarter):
    if string_of_current_quarter > "4" or string_of_current_quarter < "1":
        return "-"
    return {
        '1': _("(January - March)"),
        '2': _("(April - June)"),
        '3': _("(July - September)"),
        '4': _("(October - December)"),
    }[string_of_current_quarter]


def AboutView(request):
    template_name = 'osschallenge/about.html'
    return render(request, template_name, {
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

    def generate_key(self):
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
