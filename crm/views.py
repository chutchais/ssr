from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
import os.path
from django.conf import settings

import xlrd
import re

from django.db.models import Q,F
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.edit import FormMixin

from .forms import BookingFileForm,ExtraChargeFileForm,BookingForm,BookingInvoiceForm
from .models import (Agent,
					BillTo,
					Booking,
					BookingFile,
					Customer,
					Container,
					Extra_Charge,
					Line,
					Vessel,
					Vip)
# Create your views here.
# class FilteredListView(FormMixin, ListView):
# 	def get_form_kwargs(self):
# 		return {
# 			'initial': self.get_initial(),
# 			'prefix': self.get_prefix(),
# 			'data': self.request.GET or None
# 		}

# 	def get(self, request, *args, **kwargs):
# 		self.object_list = self.get_queryset()

# 		form = self.get_form(self.get_form_class())

# 		if form.is_valid():
# 			self.object_list = form.filter_queryset(request, self.object_list)

# 		context = self.get_context_data(form=form, object_list=self.object_list)
# 		return self.render_to_response(context)

def Home(request):
	# now = datetime.datetime.now()
	html = '<html><body>It is now %s.</body></html>' % 'Test'
	return HttpResponse(html)

def BookingFileDelete(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	bookingfile_obj = get_object_or_404(BookingFile, slug=slug)
	bookingfile_obj.delete()
	return redirect('../')

def BookingFileVip(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	from django.db.models import Avg,Min,Max
	bookingfiles = get_object_or_404(BookingFile, slug=slug)
	for booking_obj in bookingfiles.booking_set.all():
		#find Min Date-In,line,customer
		booking_obj.perform_charge()
		# booking = booking_obj.name
		# line = booking_obj.line
		# customer = booking_obj.customer
		# datein = booking_obj.container_set.all().aggregate(Min('in_date'))['in_date__min']
		# vip = get_vip(line,customer,datein)
		# if vip:
		# 	booking_obj.vip = vip
		# 	booking_obj.save()
		# 	# print (booking,line,customer,vip)
		# 	for c in booking_obj.container_set.all():
		# 		c.update_charge()
		# 		c.save()
		# 		print('%s -- charge : %s day(s)' % (c.number,c.charge))
	return redirect(reverse_lazy( 'crm:detail', kwargs={'slug': slug}))

def get_vip(line,customer,datein):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	vip = Vip.objects.filter(line=line,
							consignee=customer,
							start_date__lte = datein ,end_date__gte = datein)
	if vip :
		return vip.first()
	return None

def BookingFileProcess(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	bookingfile_obj = get_object_or_404(BookingFile, slug=slug)
	book = xlrd.open_workbook(file_contents=bookingfile_obj.name.read())
	xl_sheet = book.sheet_by_index(0)
	# print ('Sheet name: %s' % xl_sheet.name)
	# print ('Total row %s' % xl_sheet.nrows )
	# print ('Total col %s' % xl_sheet.ncols)

	col_cont_ix = 9 #Container Column index
	regex='^[A-Z]{4}[0-9]{7}$'
	vVessel=''
	vVoy=''
	vLine=''
	vAgent=''
	vBill=''
	vBooking=''
	vCustomer=''
	vIso=''
	vLength=0
	vIn =''
	vOut =''
	vDWell =''
	from datetime import datetime

	for row_index in range(0, xl_sheet.nrows):
		vContainer = xl_sheet.cell(row_index, col_cont_ix).value.__str__().strip()

		if (vContainer !='' and re.match(regex,vContainer)) :
			vVessel=	xl_sheet.cell(row_index, 0).value.__str__().strip()
			vVoy=		xl_sheet.cell(row_index, 3).value.__str__().strip()
			vLine=		xl_sheet.cell(row_index, 4).value.__str__().strip()
			vAgent=		xl_sheet.cell(row_index, 5).value.__str__().strip()
			vBill=		xl_sheet.cell(row_index, 6).value.__str__().strip()
			vBooking=	xl_sheet.cell(row_index, 7).value.__str__().strip()
			vCustomer=	xl_sheet.cell(row_index, 8).value.__str__().strip()
			vIso=		xl_sheet.cell(row_index, 10).value.__str__().strip()
			vLength=	xl_sheet.cell(row_index, 11).value.__str__().strip()
			vIn =		xl_sheet.cell(row_index, 12).value.__str__().strip()
			vOut =		xl_sheet.cell(row_index, 13).value.__str__().strip()
			vDWell =	xl_sheet.cell(row_index, 14).value.__str__().strip()
			# print (row_index,vVessel,vVoy,vLine,vAgent,vContainer)
			# 1 -- create Vessel
			vessel,created = Vessel.objects.get_or_create(name=vVessel)
			#2 -- Line
			line,created = Line.objects.get_or_create(name=vLine)
			#3 -- Agent
			agent,created = Agent.objects.get_or_create(name=vAgent)
			#4 -- BillTo
			billto,created = BillTo.objects.get_or_create(name=vBill)
			#5 -- Customer
			vCustomer = vCustomer.split('/')[0].strip()
			customer,created = Customer.objects.get_or_create(name=vCustomer)

			#6 --create Booking
			booking,created = Booking.objects.get_or_create(name=vBooking,voy=vVoy)
			if created :
				booking.booking_file= bookingfile_obj
				booking.vessel 		= vessel
				booking.agent 		= agent 
				booking.line 		= line
				booking.billed_to 	= billto
				booking.customer 	= customer
				booking.company     = bookingfile_obj.company

				booking.save()

			# Create Container
			container,created = Container.objects.get_or_create(number=vContainer,booking=booking)
			if created :
				container.iso				= vIso
				container.container_size	= vLength
				container.in_date			= datetime.strptime(vIn,'%d/%m/%Y') #String To Date
				container.out_date			= datetime.strptime(vOut,'%d/%m/%Y') #String To Date
				container.dwell				= vDWell
				container.save()


			# Update Booking File
			
			bookingfile_obj.uploaded = True
			bookingfile_obj.upload_date = datetime.now()
			# Finding VIP that match with Start and End time, Line and Customer
			# booking,created = Booking.objects.get_or_create(name=vBooking,voy=vVoy)
			# Find Min Date-In

			# vip,created = Vip.objects.filter(name=vCustomer)
			#------------------------------------------------------------------
			bookingfile_obj.save()

	return redirect(reverse_lazy( 'crm:detail', kwargs={'slug': slug}))

	# return render(
 #        request,
 #        'crm/bookingfile_detail.html',
 #        {
 #        	'object':bookingfile_obj
 #        })


class BookingFileListView(LoginRequiredMixin,ListView):
	model = BookingFile
	paginate_by = 30
	template_name = 'bookingfile_list.html'
	

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return BookingFile.objects.filter(name__icontains=query)
		return BookingFile.objects.all()

	# form_class=PersonSearchForm

	# def get_form_kwargs(self):
	# 	return {
	# 		'initial': self.get_initial(),
	# 		'prefix': self.get_prefix(),
	# 		'data': self.request.GET or None
	# 	}
	
	# def get(self, request, *args, **kwargs):
	# 	self.object_list = self.get_queryset()

	# 	form = self.get_form(self.get_form_class())

	# 	if form.is_valid():
	# 		self.object_list = form.filter_queryset(request, self.object_list)

	# 	context = self.get_context_data(form=form, object_list=self.object_list)
	# 	return self.render_to_response(context)

	# def get_context_data(self, **kwargs):
	# 	context = super(BookingFileListView, self).get_context_data(**kwargs) 
	# 	list_file = BookingFile.objects.all()
	# 	paginator = Paginator(list_file, self.paginate_by)

	# 	page = self.request.GET.get('page')

	# 	try:
	# 		file_exams = paginator.page(page)
	# 	except PageNotAnInteger:
	# 		file_exams = paginator.page(1)
	# 	except EmptyPage:
	# 		file_exams = paginator.page(paginator.num_pages)

	# 	context['object_list'] = file_exams
	# 	return context

class BookingFileDetailView(LoginRequiredMixin,DetailView):
	model = BookingFile
	template_name = 'crm/bookingfile_detail.html'

	def get_context_data(self, **kwargs):
		context = super(BookingFileDetailView, self).get_context_data(**kwargs)
		# context['now'] = timezone.now()
		print (kwargs)
		print(self.kwargs.get('slug'))
		return context



class BookingFileCreateView(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	permission_required = 'crm.can_upload_file'
	template_name = 'form.html'
	form_class = BookingFileForm

	# def form_valid(self,form):
	# 	voy = get_object_or_404(Voy, slug=self.kwargs.get('slug'))
	# 	form.instance.voy = voy
	# 	obj = form.save(commit=False)
	# 	return super(CutOffCreateView,self).form_valid(form)

	# def get_initial(self):
	# 	# print ('get_initial %s' % self.kwargs)
	# 	voy = get_object_or_404(Voy, slug=self.kwargs.get('slug'))
	# 	return {'voy':voy}

	def get_form_kwargs(self):
		kwargs = super(BookingFileCreateView,self).get_form_kwargs()
		# kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
		# print ('Kwarg %s' % self.request)
		
		return kwargs

		# def get_form_kwargs(self):
  #       kwargs = super(FolderCreate, self).get_form_kwargs()
  #       kwargs['user'] = self.request.user
  #       return kwargs

	# # def get_queryset(self):
	# # 	return Item.objects.filter(user=self.request.user)
	# def get_queryset(self):
	# 	qs = super(BookingFileCreateView, self).get_queryset()
	# 	return qs.filter(voy__vessel__v_type='VESSEL')

	def get_context_data(self,*args,**kwargs):
		context = super(BookingFileCreateView,self).get_context_data(*args,**kwargs)
		context['title']='Upload Booking List File'
		return context


# Booking Details
class BookingListView(LoginRequiredMixin,ListView):
	model = Booking
	paginate_by = 30
	template_name = 'booking_list.html'

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Booking.objects.filter(Q(name__icontains=query)|
				Q(ssr_code__icontains=query)|
				Q(voy__icontains=query)|
				Q(line__name__icontains=query)|
				Q(vessel__name__icontains=query)|
				Q(company__name__icontains=query)|
				Q(customer__name__icontains=query)|
				Q(invoice__icontains=query)).order_by('-id')
		return Booking.objects.all().order_by('-id')

class BookingDetailView(LoginRequiredMixin,DetailView):
	model = Booking
	template_name = 'crm/booking_detail.html'

	def get_context_data(self, **kwargs):
		context = super(BookingDetailView, self).get_context_data(**kwargs)
		# context['now'] = timezone.now()
		# print (kwargs)
		print(self.kwargs.get('slug'))
		return context

def BookingVip(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	from django.db.models import Avg,Min,Max
	booking = get_object_or_404(Booking, slug=slug)
	booking.perform_charge()
	# Get ETB from Auto berth System
	vessel_code =  booking.vessel.code
	voy 		=  booking.voy
	print('Get ETB from autoberth : %s - %s' % (vessel_code,voy))
	etb = getETB(vessel_code,voy)
	if etb != '':
		booking.etb = etb
		booking.save()
	# print('Returned etb : %s' % etb)
	# ------------------------------
	print ('Re-cal VIP')
	return redirect(reverse_lazy('crm:booking-detail', kwargs={'slug': slug}))

def getETB(vessel_code,voy):
	import urllib3
	http = urllib3.PoolManager()
	url = 'http://192.168.10.20:8003/berth/etb/%s/%s/' % (vessel_code,voy)
	r = http.request('GET',url )
	if r.status == 200:
		return r.data.decode("utf-8")
	else:
		return ''


def BookingSendApprove(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	if not request.user.has_perm('crm.can_send_approve'):
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	from django.db.models import Avg,Min,Max
	booking = get_object_or_404(Booking, slug=slug)
	booking.draft=False
	booking.save()

	return redirect(reverse_lazy( 'crm:booking-list'))

def BookingResetVip(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
		
	from django.db.models import Avg,Min,Max
	booking = get_object_or_404(Booking, slug=slug)
	booking.clear_vip()
	return redirect(reverse_lazy( 'crm:booking-detail', kwargs={'slug': slug}))

class ExtraChargeDeleteView(LoginRequiredMixin,DeleteView):
	model = Extra_Charge

	def get_object(self, queryset=None):
		obj = super(ExtraChargeDeleteView, self).get_object()
		# print ('Delete %s' % obj)
		return obj

	def get_success_url(self):
	# Assuming there is a ForeignKey from Comment to Post in your model
		# booking = self.object.voy 
		# print (voy)
		return reverse_lazy( 'crm:booking-detail', kwargs={'slug': self.object.booking.slug})

class ExtraChargeUpdateView(LoginRequiredMixin,UpdateView):
	model = Extra_Charge
	template_name = 'form.html'
	form_class = ExtraChargeFileForm

	def get_form_kwargs(self):
		kwargs = super(ExtraChargeUpdateView,self).get_form_kwargs()
		kwargs['slug'] = self.kwargs.get('slug')
		# kwargs['booking'] = Booking.objects.get(slug=self.kwargs.get('slug'))
		return kwargs

	def get_context_data(self,*args,**kwargs):
		context = super(ExtraChargeUpdateView,self).get_context_data(*args,**kwargs)
		context['title']='Edit Extra Charge'
		return context

	def get_success_url(self,*args, **kwargs):
		slug = self.kwargs.get('slug')
		extra = Extra_Charge.objects.get(slug=slug)
		# booking_slug = Booking.objects.get(slug=extra.booking.slug)
		url = reverse('crm:booking-detail',kwargs={'slug':extra.booking.slug})
		return url

class ExtraChargeCreateView(LoginRequiredMixin,CreateView):
	template_name = 'form.html'
	form_class = ExtraChargeFileForm

	def get_form_kwargs(self):
		kwargs = super(ExtraChargeCreateView,self).get_form_kwargs()
		kwargs['slug'] = self.kwargs.get('slug')
		# kwargs['booking'] = Booking.objects.get(slug=self.kwargs.get('slug'))
		return kwargs

	# def get_initial(self):
	# 	booking = get_object_or_404(Booking, slug=self.kwargs.get('slug'))
	# 	# print(booking)
	# 	return {
	# 		'book':booking,
	# 	}

	def get_context_data(self,*args,**kwargs):
		context = super(ExtraChargeCreateView,self).get_context_data(*args,**kwargs)
		context['title']='Upload Extra Charge'
		return context

	def get_success_url(self,*args, **kwargs):
		slug = self.kwargs.get('slug')
		url = reverse('crm:booking-detail',kwargs={'slug':slug})
		return url

	def form_valid(self,form):
		booking = get_object_or_404(Booking, slug=self.kwargs.get('slug'))
		form.instance.booking = booking
		obj = form.save(commit=False)
		return super(ExtraChargeCreateView,self).form_valid(form)


class BookingUpdateView(LoginRequiredMixin,UpdateView):
	model = Booking
	template_name = 'form.html'
	form_class = BookingForm
	

	#  return a dictionary with the kwargs that will be passed to the __init__ of your form
	def get_form_kwargs(self):
		kwargs = super(BookingUpdateView,self).get_form_kwargs()
		redirect = self.request.GET.get('next')
		print (redirect)

		if redirect:
			if 'initial' in kwargs.keys():
				kwargs['initial'].update({'next': redirect})
			else:
				kwargs['initial'] = {'next': redirect}
		return kwargs

	def get_success_url(self,*args, **kwargs):
		slug = self.kwargs.get('slug')
		# Original
		# url = reverse('crm:booking-detail',kwargs={'slug':slug})
		url = reverse('crm:booking-list')
		return url
		# return url

	# Passing Data to Template
	def get_context_data(self,*args,**kwargs):
		context = super(BookingUpdateView,self).get_context_data(*args,**kwargs)
		context['title']='Change SSR Code and Confirmation'
		context['next']= self.request.GET.get('next')
		return context

class BookingInvoiceUpdateView(LoginRequiredMixin,UpdateView):
	model = Booking
	template_name = 'form.html'
	form_class = BookingInvoiceForm
	

	#  return a dictionary with the kwargs that will be passed to the __init__ of your form
	def get_form_kwargs(self):
		kwargs = super(BookingInvoiceUpdateView,self).get_form_kwargs()
		redirect = self.request.GET.get('next')
		print (redirect)

		if redirect:
			if 'initial' in kwargs.keys():
				kwargs['initial'].update({'next': redirect})
			else:
				kwargs['initial'] = {'next': redirect}
		return kwargs

	def get_success_url(self,*args, **kwargs):
		slug = self.kwargs.get('slug')
		# Original
		# url = reverse('crm:booking-detail',kwargs={'slug':slug})
		url = reverse('crm:booking-list')
		return url
		# return url

	# Passing Data to Template
	def get_context_data(self,*args,**kwargs):
		context = super(BookingInvoiceUpdateView,self).get_context_data(*args,**kwargs)
		context['title']='Update Invoice information'
		context['next']= self.request.GET.get('next')
		return context