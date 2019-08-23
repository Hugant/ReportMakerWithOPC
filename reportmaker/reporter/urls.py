from django.conf.urls import url

from . import views

app_name = 'reporter'
urlpatterns = [
	url('', views.index, name='index'),

	url('login/', views.user_login, name='login'),
	url('logout/', views.user_logout, name='logout'),

	url('reports/', views.ReportListView.as_view(), name='reports'),
	url('reports/create/', views.create, name='create'),
	url('reports/<int:report_id>/', views.ProcessListView.as_view(), name='report'),
	url('reports/<int:report_id>/edit/', views.edit, name='report_edit'),
	url('reports/<int:report_id>/remove/', views.remove, name='report_remove'),
]
