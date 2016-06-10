from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Task, Project


def IndexView(generic.ListView):
	template_name = 'osschallenge/index.html'
	context_object_name = 'project_list'

	def get_queryset(self):
		return Project.objects.filter
