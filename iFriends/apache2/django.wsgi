#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
# место, где лежит джанго
sys.path.append('/home/yuri/python/iFriends/apache2/')
# место, где лежит проект
sys.path.append('/home/yuri/python/')
# файл конфигурации проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'iFriends.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()