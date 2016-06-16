
from django.db import models


class Role(models.Model):
	role = models.CharField(max_length=50)


class Groups(models.Model):
	group = models.CharField(max_length=50)


class User(models.Model):
	surname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	role = models.ForeignKey(Role)
	tasks_done = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	mail = models.CharField(max_length=50)
	nickname = models.CharField(max_length=25)


class Project(models.Model):
	title = models.CharField(max_length=50)
	lead_text = models.CharField(max_length=300)
	description = models.TextField
	licence = models.CharField(max_length=50)
	website = models.CharField(max_length=50)
	github = models.CharField(max_length=50)
	owner = models.ForeignKey(User)
	mentors = models.ManyToManyField(User)


class Task(models.Model):
	title = models.CharField(max_length=50)
	lead_text = models.CharField(max_length=300)
	description = models.TextField
	mentor = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	contributers = models.ManyToManyField(User)


class Picture(models.Model):
	project = models.ForeignKey(Project)
	picture = models.CharField(max_length=50)


class Comment(models.Model):
	task = models.ForeignKey(Task)
	comment = models.CharField(max_length=150)
	author = models.ForeignKey(User)
