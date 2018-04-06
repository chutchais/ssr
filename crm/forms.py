from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Booking,BookingFile,Extra_Charge,Container,Booking


class BookingForm(ModelForm):
	class Meta:
		model = Booking
		fields = ['ssr_code','remark','draft']

	# def __init__(self, *args, **kwargs):
	# 	super(BookingForm, self).__init__(*args, **kwargs)
	# 	self.redirect = 'cc'

class BookingFileForm(ModelForm):
	class Meta:
		model = BookingFile
		fields = ['name','company','remark']


class ExtraChargeFileForm(ModelForm):
	class Meta:
		model = Extra_Charge
		fields = ['container','charge','remark','qty','status']

	def __init__(self, *args, **kwargs):
		slug = kwargs.pop('slug')
		# book = kwargs.pop('book',None)
		super(ExtraChargeFileForm, self).__init__(*args, **kwargs)
		self.fields['container'].queryset = Container.objects.filter(booking__slug=slug)
		# if book:
		# 	self.fields['booking'] = book[0]['book']

	# def save(self, commit=True):
	# 	extra_charge = super(ExtraChargeFileForm, self).save(commit=False)
	# 	# print ('Current stowage %s' % container.stowage)
	# 	print(self.fields['booking'])
	# 	extra_charge.booking =  self.fields['booking']

	# 	if commit:
	# 		extra_charge.save()
	# 	return extra_charge
		# self.fields['booking'] = booking
# class PersonSearchForm(forms.Form):
# 	query = forms.CharField(label='Filter', required=False)

# 	def filter_queryset(self, request, queryset):
# 		if self.cleaned_data['name']:
# 			return queryset.filter(name__icontains=self.cleaned_data['query'])
# 		return queryset
