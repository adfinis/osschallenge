import base64
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from django_markdown.models import MarkdownField
from django.db.models import Q
from django.db.models.signals import post_save


class Rank(models.Model):
    name = models.CharField(max_length=50)
    required_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    links = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    key = models.CharField(max_length=10, unique=True)
    picture = ThumbnailerImageField(upload_to='profile-pictures', null=True)
    rank = models.ForeignKey(Rank, default=2, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_points(self):
        approved_tasks = Task.objects.filter(
            Q(task_checked=True) &
            Q(assignee_id=self.user.id)
        ).count()
        return approved_tasks * 5


class Project(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'),)
    lead_text = models.CharField(max_length=300, verbose_name=_('Lead text'),)
    description = models.CharField(max_length=5000,
                                   verbose_name=_('Description'),)
    licence = models.CharField(max_length=50, verbose_name=_('Licence'),)
    website = models.CharField(max_length=50, verbose_name=_('Website'),)
    github = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name="project_owner",
                              verbose_name=_('Owner'), on_delete=models.CASCADE)
    mentors = models.ManyToManyField(User, related_name="project_mentors",
                                     verbose_name=_('Mentors'))
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'),)
    lead_text = models.CharField(max_length=300, verbose_name=_('Lead text'),)
    description = models.CharField(max_length=5000,
                                   verbose_name=_('Description'),)
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, null=True,
                                 related_name="assignee_tasks",
                                 verbose_name=_('Assignee'), on_delete=models.CASCADE)
    task_done = models.BooleanField(null=False, default=False)
    task_checked = models.BooleanField(null=False, default=False)
    picture = ThumbnailerImageField(upload_to='', null=True)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    approval_date = models.DateField(null=True)
    website = models.CharField(null=True, max_length=50, verbose_name=_('Website'))

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = MarkdownField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

def create_profile(sender, **kwargs):
    if kwargs["created"]:
        key = base64.b32encode(os.urandom(7))[:10].lower().decode("utf-8")
        profile = Profile(key=key, user=kwargs["instance"])
        profile.save()

post_save.connect(create_profile, sender=User)
