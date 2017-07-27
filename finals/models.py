# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

DAY_CHOICES = (
    ("MWF", "Monday, Wednesday, Friday"),
    ("TR", "Tuesday, Thursday"),
)

# Create your models here.
class Final(models.Model):
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL)
    class_name = models.CharField(max_length=100)
    class_day = models.CharField(max_length=100, choices = DAY_CHOICES, default = "MWF")
    class_time = models.TimeField()

    def __str__(self):
        return self.class_name
