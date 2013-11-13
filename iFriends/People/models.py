#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

gender_list = (('M', 'Male'), ('F', 'Female' ))

class Person(models.Model):
    name = models.CharField('name', max_length=200)
    birthday = models.DateField('Birthday', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=gender_list)
    email = models.EmailField('Email', max_length=100, unique=True)
    favoriteURL = models.URLField('myURL')
    desc = models.TextField('Desc', max_length=500, null=True)
    
    def __str__(self):
        return '%s' % (self.name)
    
    def __unicode__(self):
        return self.name
