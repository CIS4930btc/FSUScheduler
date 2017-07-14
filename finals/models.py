# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Final(models.Model):
    class_name = models.CharField(max_length=100)
    class_day = models.CharField(max_length=100)
    class_time = models.CharField(max_length=100)

    def __str__(self):
        return self.title
