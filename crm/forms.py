from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import BookingFile

class BookingFileForm(ModelForm):
	class Meta:
		model = BookingFile
		fields = ['name','company','remark']


# class PersonSearchForm(forms.Form):
# 	query = forms.CharField(label='Filter', required=False)

# 	def filter_queryset(self, request, queryset):
# 		if self.cleaned_data['name']:
# 			return queryset.filter(name__icontains=self.cleaned_data['query'])
# 		return queryset
