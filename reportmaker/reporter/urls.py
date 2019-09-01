from django.conf.urls import url

from . import views

app_name = 'reporter'

urlpatterns = [
	url(r'^$', views.index, name='index'),

	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),

	url(r'^reports/$', views.ReportListView.as_view(), name='reports'),
	url(r'^reports/create/$', views.create, name='create'),
	url(r'^reports/(?P<report_id>[0-9]+)/$', views.ProcessListView.as_view(), name='report'),
	url(r'^reports/(?P<report_id>[0-9]+)/edit/$', views.edit, name='report_edit'),
	url(r'^reports/(?P<report_id>[0-9]+)/remove/$', views.remove, name='report_remove'),
]
