# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-19 18:28
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20160919_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='categorie',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='section_name', chained_model_field='section', on_delete=django.db.models.deletion.CASCADE, to='home.Categorie'),
        ),
    ]
