from django.views import generic
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView
from .models import Task, Project, User, Profile
from .forms import TaskForm, ProjectForm


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
        form.instance.project = Project.objects.get(pk = self.kwargs['pk'])
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


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'password'
    ]
    
    def get_form(self, form_class):
        form = super(RegisterView, self).get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return form

    def form_valid(self, form):
        self.object = form.save()

        # creating profile for user
        profile = Profile()
        profile.user = self.object
        profile.save()

        return HttpResponseRedirect(self.get_success_url())

    success_url = '/login/'
