#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import HttpResponse
from People.models import Person

def index(request):
    html = "<H1>People</H1><HR>"
    return HttpResponse(html)
