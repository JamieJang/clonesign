# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-20 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_auto_20180119_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='filename',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[('서명 전', '서명 전'), ('내 서명 필요', '내 서명 필요'), ('상대 서명 필요', '상대 서명 필요'), ('완료', '완료'), ('거절', '거절'), ('취소', '취소')], default='서명 전', max_length=50),
        ),
    ]
