# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-05 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalapp', '0002_tratata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tratata',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={},
        ),
        migrations.DeleteModel(
            name='Tratata',
        ),
    ]