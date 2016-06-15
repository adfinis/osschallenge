from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(
		r'^(?P<project_id>[0-9]+)/$',
		views.ProjectView.as_view(), 
		name='project'
	),
	url(
		r'^(?P<project_id>[0-9]+)/tasks/$', 
		views.TaskIndexView.as_view(), 
		name='taskindex'
	),
	url(
		r'^(?P<project_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)', 
		views.TaskView.as_view(), 
		name='task'
	),
]
