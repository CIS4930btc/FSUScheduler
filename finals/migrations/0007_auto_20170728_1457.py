# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finals', '0006_auto_20170727_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='final',
            name='class_semester',
            field=models.CharField(choices=[('S', 'Spring'), ('F', 'Fall')], default='F', max_length=100),
        ),
        migrations.AddField(
            model_name='final',
            name='final_info',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
            preserve_default=False,
        ),
    ]
