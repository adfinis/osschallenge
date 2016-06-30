
from django.db import models


class Role(models.Model):
    role = models.CharField(max_length=50)
    
    def __str__(self):
        return self.role


class Groups(models.Model):
    group = models.CharField(max_length=50)
    
    def __str__(self):
        return self.group


class User(models.Model):
    surname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    role = models.ForeignKey(Role)
    tasks_done = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    mail = models.CharField(max_length=50)
    nickname = models.CharField(max_length=25)

    def __str__(self):
        return self.nickname


class Project(models.Model):
    title = models.CharField(max_length=50)
    lead_text = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    licence = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    github = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name = "project_owner")
    mentors = models.ManyToManyField(User, related_name = "project_mentors")

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=50)
    lead_text = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    mentor = models.ForeignKey(User, related_name = "task_mentor")
    project = models.ForeignKey(Project, related_name = "task_project")
    contributers = models.ManyToManyField(
        User, 
        related_name = "task_contributers"
    )

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
        return self.comment
