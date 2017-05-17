# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 15:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170513_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 13, 15, 18, 51, 139288), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间'),
        ),
    ]
