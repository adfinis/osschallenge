from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect

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


class EditTaskView(generic.DetailView):
    model = Task
    template_name = 'osschallenge/edittask.html'

    def get_task(request):
        if request.method == 'POST':
            form = TaskForm(request.POST)

            if form.is_valid():
                return HttpResponseRedirect('')

        else:
            form = TaskForm()

        return render(request, 'edittask.html', {'form': form})
