from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from .models import Report, Process
from .forms import ReportForm


class ReportListView(LoginRequiredMixin, generic.ListView):
	login_url = '/login'
	template_name = 'reporter/report_list.html'
	filters = {
		'id': '',
		'title': '',
		'content': '',
		'date': ''
	}

	def get_queryset(self):
		reports = Report.objects.all()
		if self.request.method == 'GET':
			self.filters['id'] = self.request.GET.get('id_filter')
			self.filters['title'] = self.request.GET.get('title_filter')
			self.filters['content'] = self.request.GET.get('content_filter')

			if self.filters['id']:
				reports = reports.filter(id=self.filters['id'])

			if self.filters['title']:
				reports = reports.filter(title_text__startswith=self.filters['title'])

			if self.filters['content']:
				reports = reports.filter(content_text__startswith=self.filters['content'])

			# TODO: filter by date

		return reports

	def get_context_data(self, **kwargs):
		context = super(ReportListView, self).get_context_data(**kwargs)
		context['filters'] = self.filters
		return context


class ProcessListView(LoginRequiredMixin, generic.ListView):
	login_url = '/login'
	template_name = 'reporter/report.html'
	filters = {
		'id': '',
		'name': '',
		'state': '',
		'ram': '',
		'date': ''
	}

	def get_queryset(self):
		processes = Process.objects.all()
		processes = processes.filter(report=self.kwargs.get('report_id'))
		if self.request.method == 'GET':
			self.filters['id'] = self.request.GET.get('id_filter')
			self.filters['name'] = self.request.GET.get('name_filter')
			self.filters['state'] = self.request.GET.get('state_filter')
			self.filters['ram'] = self.request.GET.get('ram_filter')
			self.filters['date'] = self.request.GET.get('date_filter')

			if self.filters['id']:
				processes = processes.filter(id=self.filters['id'])

			if self.filters['name']:
				processes = processes.filter(name_text__startswith=self.filters['name'])

			if self.filters['state']:
				processes = processes.filter(state_text__startswith=self.filters['state'])

			if self.filters['ram']:
				processes = processes.filter(ram_in_kb_int__startswith=int(self.filters['ram']))

			# TODO: filter by date

		return processes

	def get_context_data(self, **kwargs):
		context = super(ProcessListView, self).get_context_data(**kwargs)
		context['filters'] = self.filters
		context['report'] = get_object_or_404(Report, id=self.kwargs.get('report_id'))
		return context


def index(request):
	return render(request, 'reporter/index.html')


@login_required()
def report(request, report_id):
	report = get_object_or_404(Report, id=report_id)
	return render(request, 'reporter/report.html', {'report': report})


@login_required()
def remove(request, report_id):
	if request.method == 'POST':
		Report.objects.get(id=report_id).delete()
		return HttpResponseRedirect('/reports/')
	else:
		return render(request, 'reporter/remove.html')


@login_required()
def create(request):
	import updater
	import OpenOPC

	if request.method == 'POST':
		form = ReportForm(request.POST)
		if form.is_valid():
			title = request.POST.get('title_text')
			content = request.POST.get('content_text')
			pub = timezone.now()
			report = Report(title_text=title, content_text=content, pub_date=pub)
			report.save()
			#
			# opc = OpenOPC.client()
			# opc.connect('Matrikon.OPC.Simulation')
			# process = opc.read('Random.Int4')
			# process_name = report.title_text + " - " + "process #" + str(Process.objects.all().filter(report=report.id).distinct().count())
			# process = Process(
			# 	report_id=report.id,
			# 	name_text=process_name,
			# 	state_text=process[1],
			# 	ram_in_kb_int=process[0],
			# 	date=timezone.now())
			# process.save()
			# print(process)
			# report.process_set.add(process)
			# print('created')

			updater.start()
			return HttpResponseRedirect('/reports/' + str(report.id))
	else:
		return render(request, 'reporter/create.html')


@login_required()
def edit(request, report_id):
	report = get_object_or_404(Report, id=report_id)
	if request.method == 'POST':
		report.title_text = request.POST.get('title_text')
		report.content_text = request.POST.get('content_text')
		report.save()
		return HttpResponseRedirect('/reports/')
	else:
		return render(request, 'reporter/edit.html', {'report': report})


def user_login(request):
	next_page = ""
	if request.method == 'GET':
		next_page = request.GET.get('next')

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				print(next_page)
				if next_page != "":
					return HttpResponseRedirect(next_page)
				else:
					return HttpResponseRedirect('/reports/')
			else:
				message = "User ' + user.username + ' is not active, create new user"
		else:
			message = "Incorrect username or password"

		return render(request, 'reporter/login.html', {'message': message, 'username': username})
	else:
		return render(request, 'reporter/login.html')


def user_logout(request):
	logout(request)
	return HttpResponseRedirect('')

