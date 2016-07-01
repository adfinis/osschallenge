from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404

from .models import Task, Project
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
