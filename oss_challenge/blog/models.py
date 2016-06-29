from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    lead_text = models.CharField(max_length=300)
    content = models.CharField(max_length=1000)
    author = models.CharField(max_length=50)
