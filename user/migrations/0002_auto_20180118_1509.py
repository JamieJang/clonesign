# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-18 06:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='name',
            new_name='username',
        ),
    ]