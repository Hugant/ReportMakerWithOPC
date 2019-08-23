from django import forms


class ReportForm(forms.Form):
	title_text = forms.CharField(label='title', max_length=200)
	content_text = forms.CharField(label='content', max_length=1000)
