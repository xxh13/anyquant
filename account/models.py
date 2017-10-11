#-*- coding:utf-8 -*-
__author__ = 'cheng'

from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)

    email = models.CharField(max_length=200)
    name = models.CharField(max_length=100)

    password = models.CharField(max_length=100)

    is_active = models.BooleanField()
    active_code = models.CharField(max_length=100)

    class Meta:
        db_table = 'account'