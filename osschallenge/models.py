from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from django_markdown.models import MarkdownField
from django.db.models import Q


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Rank(models.Model):
    name = models.CharField(max_length=50)
    required_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Groups(models.Model):
    group = models.CharField(max_length=50)

    def __str__(self):
        return self.group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, default=1)
    links = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    key = models.CharField(max_length=10, unique=True)
    picture = ThumbnailerImageField(upload_to='profile-pictures', null=True)
    rank = models.ForeignKey(Rank, default=2)

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
                              verbose_name=_('Owner'),)
    mentors = models.ManyToManyField(User, related_name="project_mentors",
                                     verbose_name=_('Mentors'),)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'),)
    lead_text = models.CharField(max_length=300, verbose_name=_('Lead text'),)
    description = models.CharField(max_length=5000,
                                   verbose_name=_('Description'),)
    project = models.ForeignKey(Project, related_name="tasks")
    assignee = models.ForeignKey(User, null=True,
                                 related_name="assignee_tasks",
                                 verbose_name=_('Assignee'),)
    task_done = models.BooleanField(null=False, default=False)
    task_checked = models.BooleanField(null=False, default=False)
    picture = ThumbnailerImageField(upload_to='', null=True)
    approved_by = models.ForeignKey(User, null=True)
    approval_date = models.DateField(null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task)
    comment = MarkdownField(max_length=150)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
