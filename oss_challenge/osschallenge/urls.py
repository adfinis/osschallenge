from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from forms import LoginForm

urlpatterns = [
    url(r'^$',
        views.IndexView,
        name='index'),

    url(r'^projects/new_project/$',
        views.NewProjectView.as_view(),
        name='newproject'),

    url(r'^projects/$',
        views.ProjectIndexView.as_view(),
        name='projectindex'),

    url(r'^projects/(?P<pk>[0-9]+)/$',
        views.ProjectView.as_view(),
        name='project'),

    url(r'^projects/(?P<pk>[0-9]+)/edit/$',
        views.EditProjectView,
        name='editproject'),

    url(r'^projects/(?P<pk>[0-9]+)/new_task/$',
        views.NewTaskView.as_view(),
        name='newtask'),

    url(r'^tasks/$',
        views.TaskIndexView.as_view(),
        name='taskindex'),

    url(r'^tasks/(?P<pk>[0-9]+)/$',
        views.TaskView.as_view(),
        name='task'),

    url(r'^tasks/(?P<pk>[0-9]+)/edit/$',
        views.EditTaskView,
        name='edittask'),

    url(r'^profile/$',
        views.ProfileView,
        name='profile'),

    url(r'^ranking/$',
        views.RankingView.as_view(),
        name='ranking'),

    url(r'^register/$',
        views.RegistrationView.as_view()),

    url(r'^registration_done/(?P<key>[\w\.-]+)/',
        views.RegistrationDoneView.as_view()),

    url(r'^registration_send_mail/$',
        views.RegistrationSendMailView.as_view()),

    url(r'^password_change/$', auth_views.password_change,
        name='password_change'),

    url(r'^password_change_done/$',
        auth_views.password_change_done, name='password_change_done'),

    url(r'^password_reset/$', auth_views.password_reset,
        name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),

    url(r'^login/$', auth_views.login, {'authentication_form': LoginForm},
        name='login'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
