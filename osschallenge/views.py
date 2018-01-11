import base64
import os
import time
import bisect
from django.views import generic
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from .models import Task, Project, Profile, Comment, Rank
from django.contrib.auth.models import User, Group
from .forms import TaskForm, ProjectForm, ProfileForm, UserForm, CommentForm
from django.views.generic import FormView
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count, Case, When
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def IndexView(request):
    template_name = 'osschallenge/index.html'

    return render(request, template_name)


class NewProjectView(CreateView):
    model = Project
    template_name = 'osschallenge/newproject.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewProjectView, self).form_valid(form)
    success_url = '/projects/'


def mentor_check(group_id):
    try:
        mentor_id = Group.objects.get(name="Mentor").id
    except Group.DoesNotExist:
        return False
    if mentor_id == group_id:
        return True
    return False


def contributor_check(group_id):
    try:
        contributor_id = Group.objects.get(name="Contributor").id
    except Group.DoesNotExist:
        return False
    if contributor_id == group_id:
        return True
    return False


def ProjectIndexView(request):
    project_list = Project.objects.filter(active=True).order_by('id')
    template_name = 'osschallenge/projectindex.html'
    try:
        mentor = mentor_check(request.user.groups.get().id)
    except Group.DoesNotExist:
        mentor = False
    if request.GET.get('page'):
        current_page = request.GET.get('page')
    else:
        current_page = 1
    projects, last_page, current_page = paging(current_page, project_list, 4)
    return render(request, template_name, {
        'mentor': mentor,
        'projects': projects,
        'current_page': current_page,
        'last_page': last_page,
    })


def ProjectView(request, pk):
    project = Project.objects.get(pk=pk)
    task_objects = Task.objects.filter(project_id=project.id)
    task_list = []
    for obj in task_objects:
        task_list.append(obj)
    mentors = project.mentors.all()
    owner = project.owner
    current_user_id = request.user.id
    can_create_new_tasks = project.mentors.filter(id=current_user_id)
    template_name = 'osschallenge/project.html'

    return render(request, template_name, {
        'project': project,
        'mentors' : mentors,
        'owner' : owner,
        'current_user_id': current_user_id,
        'can_create_new_tasks': can_create_new_tasks,
        'task_list': task_list
    })


def EditProjectView(request, pk):
    project = Project.objects.get(pk=pk)

    if 'delete-project' in request.POST:
        project.active = False
        project.save()
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


def TaskIndexView(request, username=None):
    template_name = 'osschallenge/taskindex.html'
    title = ""
    try:
        mentor = mentor_check(request.user.groups.get().id)
    except Group.DoesNotExist:
        mentor = False
    if request.user.id is not None and rankup_check(request.user) is True:
        return redirect('/rankup/')
    search = request.GET.get('search') if request.GET else None
    if username is not None:
        title = _("My Tasks")
        current_user_id = request.user.id
        user_task_objects = Task.objects.filter(
            assignee_id=current_user_id
        )
        matches = user_task_objects.order_by('id')
    elif str(request.path) == '/tasks/admin/':
        title = _("Tasks to review")
        user = request.user
        matches = Task.objects.filter(
            Q(project__mentors__id=user.id) &
            Q(task_done=True) &
            Q(task_checked=False)
        )
        matches = matches.order_by('id')
    else:
        title = _("All Tasks")
        matches = Task.objects.all().order_by('id')

    if search:
        matches = matches.filter(
            Q(title__icontains=request.GET.get('search')) |
            Q(project__title__icontains=request.GET.get('search'))
        ).distinct().order_by('id')

    if request.GET.get('page'):
        current_page = request.GET.get('page')
    else:
        current_page = 1

    tasks, last_page, current_page = paging(current_page, matches, 5)
    return render(request, template_name, {
        'tasks': tasks,
        'last_page': last_page,
        'current_page': current_page,
        'mentor': mentor,
        'username': username,
        'title': title
    })


def TaskView(request, pk):
    task = Task.objects.get(pk=pk)
    try:
        mentor_id = Group.objects.get(name="Mentor").id
        contributor = contributor_check(request.user.groups.get().id)
    except Group.DoesNotExist:
        mentor_id = 0
        contributor = False
    template_name = 'osschallenge/task.html'
    notification = ""
    render_params = {}
    if request.user.id:
        user = request.user
        project = Project.objects.get(pk=task.project_id)
        render_params['user'] = User.objects.get(pk=request.user.id)
        render_params['mentor_id'] = mentor_id
        render_params['contributor'] = contributor
        render_params['mentors'] = project.mentors.all()
        render_params['is_mentor_of_this_task'] = project.mentors.filter(
            id=user.id
        )

        if 'Claim' in request.POST:
            if task.assignee_id is None:
                task.assignee_id = user.id
                task.save()

        elif 'Release' in request.POST:
            if task.assignee_id is not None:
                task.assignee_id = None
                task.task_done = False
                task.save()

        elif 'Task done' in request.POST:
            if task.task_done is not True:
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
                comment.author_id = user.id
                comment = form.save()

        elif 'Delete-comment' in request.POST:
            comment_id = (request.POST['Delete-comment'])
            comment = Comment.objects.get(id=comment_id)
            if comment.author_id == request.user.id:
                comment.delete()

        elif 'Approve' in request.POST:
            if task.task_checked is not True:
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
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user_id=user.id)
    except (Profile.DoesNotExist, User.DoesNotExist):
        return render(request, 'osschallenge/no_profile_available.html')

    try:
        mentor = mentor_check(request.user.groups.get().id)
        contributor = contributor_check(request.user.groups.get().id)
    except Group.DoesNotExist:
        mentor = False
        contributor = False

    if request.user.id is not None and rankup_check(request.user) is True:
        return redirect('/rankup/')

    template_name = 'osschallenge/profile.html'
    total_points = profile.get_points()
    matches = Rank.objects.filter(
        required_points__lte=total_points
    ).order_by('-required_points')
    rank = matches.first()
    finished_tasks = Task.objects.filter(task_done=True)
    finished_task_list = []
    for obj in finished_tasks:
        finished_task_list.append(obj)
    if user.is_active is False:
        return render(request, 'osschallenge/profile_does_not_exist.html')

    return render(request, template_name, {
        'contributor': contributor,
        'mentor': mentor,
        'finished_task_list': finished_task_list,
        'profile': profile,
        'user': user,
        'total_points': total_points,
        'rank': rank
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


def get_quarter_start():
    """
    returns beginning of current quarter
    """
    quarters = range(1, 12, 3)
    month = int(time.strftime("%m"))

    quarter = bisect.bisect(quarters, month)
    today = date.today()
    quarter_start = [today.year, quarters[quarter - 1], 1]
    aware_date = date(
        *quarter_start
    )
    return aware_date


def get_next_quarter():
    """
    returns beginning of next quarter
    """
    return get_quarter_start() + relativedelta(months=3)


def RankingView(request):
    quarters = range(1, 12, 3)
    month = int(time.strftime("%m"))

    quarter = bisect.bisect(quarters, month)
    quarter_month = get_quarter_months(str(quarter))
    try:
        contributor_id = Group.objects.get(name="Contributor").id
    except Group.DoesNotExist:
        contributor_id = 1
    contributors = User.objects.filter(groups__id=contributor_id)
    # for every finished task add 5 points
    contributors_with_points = contributors.annotate(
        task_count=Count(
            Case(
                When(
                    assignee_tasks__task_checked=True,
                    then=1
                )
            )
        ) * 5,
        quarter_count=Count(
            Case(
                When(
                    Q(assignee_tasks__task_checked=True) & Q(
                        assignee_tasks__approval_date__lt=get_next_quarter()
                    ) & Q(
                        assignee_tasks__approval_date__gte=get_quarter_start()
                    ),
                    then=1
                )
            )
        ) * 5
    )
    ranking_list = contributors_with_points.order_by(
        '-task_count',
        'username'
    )
    if request.GET.get('page'):
        current_page = request.GET.get('page')
    else:
        current_page = 1
    users, last_page, current_page = paging(current_page, ranking_list, 10)

    template_name = 'osschallenge/ranking.html'
    return render(request, template_name, {
        'ranking_list': ranking_list,
        'quarter': quarter,
        'quarter_month': quarter_month,
        'users': users,
        'last_page': last_page,
        'current_page': current_page,
    })


def paging(page, ordered_item_list, page_sum):
    paginator = Paginator(ordered_item_list, page_sum)
    last_page = paginator.num_pages
    try:
        paged_elements = paginator.page(page)
    except PageNotAnInteger:
        paged_elements = paginator.page(1)
    except EmptyPage:
        paged_elements = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    return (paged_elements, last_page, page)


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
    return render(request, template_name)


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

        u = User.objects.get(email=form.data['email'])
        group = Group.objects.get(pk=1)
        group.user_set.add(u)

        if user is not None:
            self.generate_profile(user, group)

        return super(RegistrationView, self).form_valid(form)

    def generate_key(self):
        return base64.b32encode(os.urandom(7))[:10].lower()

    def generate_profile(self, user, group):
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
                request.template_name = (
                    'osschallenge/user_is_already_active.html')
            else:
                profile.user.is_active = True
                profile.user.save()
        else:
            request.template_name = 'osschallenge/registration_failed.html'


class RegistrationSendMailView(generic.TemplateView):
    template_name = 'osschallenge/registration_send_mail.html'


def RankupView(request):
    template_name = 'osschallenge/rankup.html'
    try:
        user = User.objects.get(username = request.user.username)
        profile = Profile.objects.get(user_id=user.id)
        needed_points = Rank.objects.get(id=profile.rank_id).required_points
        actual_points = profile.get_points()
    except (ObjectDoesNotExist, IndexError):
        return redirect('/login', permanent=True)

    if actual_points >= needed_points:
        profile.rank = Rank.objects.filter(
            required_points__gt=profile.rank.required_points
        ).order_by('required_points')[0]
        profile.save()

    return render(request, template_name, {
        'user': user.username,
        'total_points': actual_points,
    })


def rankup_check(user):
    profile = user.profile
    actual_points = profile.get_points()
    profile_points = Rank.objects.get(id=profile.rank_id).required_points

    if profile_points <= actual_points:
        return True

    return False
