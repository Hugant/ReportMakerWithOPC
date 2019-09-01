# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Report
from .models import Process

admin.site.register(Report)
admin.site.register(Process)