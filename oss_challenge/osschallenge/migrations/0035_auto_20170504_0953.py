# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 07:53
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('osschallenge', '0034_auto_20170504_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='picture',
            field=sorl.thumbnail.fields.ImageField(default=b'/home/jonas/gitty/work/oss-challenge.src/oss_challenge/osschallenge/pictures/example.jpg', upload_to=b'/home/jonas/gitty/work/oss-challenge.src/oss_challenge/osschallenge/pictures'),
        ),
    ]
