from django.views import generic
from django.shortcuts import redirect, render

from .models import Task, Project
from .forms import TaskForm


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


def EditTaskView(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save()
            return redirect('task.html', pk=task.pk)

    else:
        form = TaskForm()

    return render(request, 'osschallenge/edittask.html', {'form': form})
