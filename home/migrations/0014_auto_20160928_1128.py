# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-28 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20160923_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articl',
            name='height_field',
            field=models.IntegerField(default=700),
        ),
        migrations.AlterField(
            model_name='articl',
            name='width_field',
            field=models.IntegerField(default=1024),
        ),
    ]
