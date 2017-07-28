# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import datetime

DAY_CHOICES = (
    ("MWF", "Monday, Wednesday, Friday"),
    ("TR", "Tuesday, Thursday"),
)
SEMESTER_CHOICES= (
    ("S", "Spring"),
    ("F", "Fall"),
)

TIME_CHOICES = (
    ("a.m." , "AM"),
    ("p.m.", "PM"),
)

# Create your models here.
class Final(models.Model):
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL)
    class_name = models.CharField(max_length=100)
    class_semester = models.CharField(max_length=100, choices = SEMESTER_CHOICES, default = "F")
    class_day = models.CharField(max_length=100, choices = DAY_CHOICES, default = "MWF")
    class_time = models.TimeField()
    class_timeframe = models.CharField(max_length=100, choices = TIME_CHOICES, default = "a.m.")
    final_info = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name
