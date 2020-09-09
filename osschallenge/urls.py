from django.conf.urls import include
from django.urls import re_path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import handler404, handler500


urlpatterns = [

    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    re_path(r'^admin/', admin.site.urls),

    re_path(r'^$',
        views.IndexView,
        name='index'),

    re_path(r'^projects/new_project/$',
        views.NewProjectView.as_view(),
        name='newproject'),

    re_path(r'^projects/$',
        views.ProjectIndexView,
        name='projectindex'),

    re_path(r'^projects/(?P<pk>[0-9]+)/$',
        views.ProjectView,
        name='project'),

    re_path(r'^projects/(?P<pk>[0-9]+)/edit/$',
        views.EditProjectView,
        name='editproject'),

    re_path(r'^projects/(?P<pk>[0-9]+)/new_task/$',
        views.NewTaskView,
        name='newtask'),

    re_path(r'^tasks/(?P<pk>[0-9]+)/$',
        views.TaskView,
        name='task'),

    re_path(r'^tasks/$',
        views.TaskIndexView,
        name='taskindex'),

    re_path(r'^my_tasks/(?P<username>[0-9A-Za-z_\-\.\+\@]+)/$',
        views.TaskIndexView,
        name='mytask'),

    re_path(r'^tasks/admin/$',
        views.TaskIndexView,
        name='admin'),

    re_path(r'^tasks/(?P<pk>[0-9]+)/edit/$',
        views.EditTaskView,
        name='edittask'),

    re_path(r'^profile/edit/$',
        views.EditProfileView,
        name='editprofile'),

    re_path(r'^profile/(?P<username>[0-9A-Za-z_\-\.\+\@]+)/$',
        views.ProfileView,
        name='profile'),

    re_path(r'^ranking/$',
        views.RankingView,
        name='ranking'),

    re_path(r'^about/$',
        views.AboutView,
        name='about'),

    re_path(r'^register/$',
        views.RegistrationView.as_view(),
        name='register'),

    re_path(r'^registration_done/(?P<key>[\w\.-]+)/',
        views.RegistrationDoneView.as_view(),
        name='registrationdone'),

    re_path(r'^registration_send_mail/$',
        views.RegistrationSendMailView.as_view(),
        name='registrationsendmail'),

    re_path(r'^rankup/$',
        views.RankupView,
        name='rankup'),

    re_path(r'^password_change/$', auth_views.PasswordChangeView.as_view(),
        name='password_change'),

    re_path(r'^password_change_done/$',
        auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name='password_reset'),

    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),

    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    re_path(r'^login/$', auth_views.LoginView.as_view(authentication_form=LoginForm),
        name='login'),

    re_path(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),

    re_path(r'^markdown/', include('django_markdown.urls')),

]

handler404 = views.error_404
handler500 = views.error_500

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)  # pragma: no cover
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)  # pragma: no cover
