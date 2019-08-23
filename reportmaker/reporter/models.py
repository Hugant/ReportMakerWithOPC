# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Report(models.Model):
	title_text = models.CharField(max_length=200)
	content_text = models.CharField(max_length=1000)
	pub_date = models.DateTimeField()

	def __str__(self):
		return self.title_text


class Process(models.Model):
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	name_text = models.CharField(max_length=50)
	state_text = models.CharField(max_length=20)
	ram_in_kb_int = models.PositiveIntegerField()
	date = models.DateTimeField()

	def __str__(self):
		return self.name_text
