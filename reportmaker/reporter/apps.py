# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ReporterConfig(AppConfig):
    name = 'reporter'

    def ready(self):
        import updater
        updater.start()
