from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^projects/$', 
        views.ProjectIndexView.as_view(), 
        name='projectindex'),

    url(r'^projects/(?P<pk>[0-9]+)/$',
        views.ProjectView.as_view(), 
        name='project'),

    url(r'^projects/(?P<pk>[0-9]+)/edit/$',
        views.EditProjectView,
        name='editproject'),

    url(r'^tasks/$', 
        views.TaskIndexView.as_view(), 
        name='taskindex'),

    url(r'^tasks/(?P<pk>[0-9]+)/$', 
        views.TaskView.as_view(), 
        name='task'),

    url(r'^tasks/(?P<pk>[0-9]+)/edit/$',
        views.EditTaskView,
        name='edittask'),
]
