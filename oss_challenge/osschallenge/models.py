from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class Groups(models.Model):
    group = models.CharField(max_length=50)

    def __str__(self):
        return self.group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, default=1)
    tasks_done = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    links = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    key = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'),)
    lead_text = models.CharField(max_length=300, verbose_name=_('Lead text'),)
    description = models.CharField(max_length=5000,
                                   verbose_name=_('Description'),)
    licence = models.CharField(max_length=50, verbose_name=_('Licence'),)
    website = models.CharField(max_length=50, verbose_name=_('Website'),)
    github = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name="project_owner",
                              verbose_name=_('Owner'),)
    mentors = models.ManyToManyField(User, related_name="project_mentors",
                                     verbose_name=_('Mentors'),)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'),)
    lead_text = models.CharField(max_length=300, verbose_name=_('Lead text'),)
    description = models.CharField(max_length=5000,
                                   verbose_name=_('Description'),)
    mentor = models.ForeignKey(User, related_name="mentor_tasks")
    project = models.ForeignKey(Project, related_name="tasks")
    assignee = models.ForeignKey(User, related_name="assignee_tasks",
                                 verbose_name=_('Assignee'),)

    def __str__(self):
        return self.title


class Picture(models.Model):
    project = models.ForeignKey(Project)
    picture = models.CharField(max_length=50)

    def __str__(self):
        return self.picture


class Comment(models.Model):
    task = models.ForeignKey(Task)
    comment = models.CharField(max_length=150)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.task
