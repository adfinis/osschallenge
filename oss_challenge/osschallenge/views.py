from django.views import generic

from .models import Task, Project


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
