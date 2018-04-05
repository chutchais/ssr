from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from django.core.exceptions import ValidationError
from django.urls import reverse

from django.db.models import Count,Sum,Min,Max
from account.models import Company
# Create your models here.
ACTIVE='A'
DEACTIVE='D'
STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DEACTIVE, 'Deactive'),
    )


class BookingFile(models.Model):
	name = models.FileField(upload_to='booking/%Y/%m/%d/')
	slug = models.SlugField(unique=True,blank=True, null=True)
	company = models.ForeignKey(Company,blank=True, null=True)
	remark = models.TextField(blank=True, null=True)
	uploaded = models.BooleanField(default=False)
	upload_date = models.DateTimeField(blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return ('%s' % (self.name))

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug': self.slug})



class Vessel(models.Model):
	name = models.CharField(verbose_name ='Vessel Name',max_length=50)
	code = models.CharField(verbose_name ='Vessel Code',max_length=30,blank=True, null=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug':self.slug})

class Customer(models.Model):
	name = models.CharField(verbose_name ='Customer Name',max_length=50)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug':self.slug})

class Line(models.Model):
	name = models.CharField(verbose_name ='Line name',max_length=50)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug':self.slug})

class Agent(models.Model):
	name = models.CharField(verbose_name ='Agent name',max_length=50)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug':self.slug})

class BillTo(models.Model):
	name = models.CharField(verbose_name ='Agent name',max_length=50)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug':self.slug})

class Booking(models.Model):
	name 			= models.CharField(verbose_name ='Booking Number',max_length=50)
	ssr_code 		= models.CharField(verbose_name ='SSR Code',max_length=20,blank=True, null=True)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	booking_file 	= models.ForeignKey(BookingFile,blank=True, null=True)
	company 		= models.ForeignKey(Company,blank=True, null=True)
	voy 			= models.CharField(verbose_name ='Voyage',max_length=50,blank=True, null=True)
	line 			= models.ForeignKey('Line',blank=True, null=True)
	agent 			= models.ForeignKey('Agent',blank=True, null=True)
	customer  		= models.ForeignKey('Customer',blank=True, null=True)
	billed_to 		= models.ForeignKey('BillTo', blank=True, null=True)
	vessel  		= models.ForeignKey('Vessel', blank=True, null=True)
	vip 			= models.ForeignKey('Vip',blank=True, null=True)#ForeignKey('Vip', blank=True, null=True)
	description 	= models.CharField(max_length=255,blank=True, null=True)
	status 			= models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date 	= models.DateTimeField(auto_now_add=True)
	modified_date 	= models.DateTimeField(blank=True, null=True,auto_now=True)
	user 			= models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug':self.slug})

	def charge_total(self):
		return self.container_set.all().aggregate(Sum('charge'))['charge__sum']

	def dwell_total(self):
		return self.container_set.all().aggregate(Sum('dwell'))['dwell__sum']

	def perform_charge(self):
		first_container = self.container_set.all().first()
		vip = Vip.objects.filter(line=self.line,
							consignee=self.customer,
							start_date__lte = first_container.in_date ,
							end_date__gte = first_container.in_date)
		if vip:
			self.vip = vip.first()
			self.save()
			# print (booking,line,customer,vip)
			for c in self.container_set.all():
				c.update_charge()
				c.save()

		pass

	def clear_vip(self):
		self.vip = None
		self.save()
		for c in self.container_set.all():
				c.charge=0
				c.rate1=0
				c.rate2=0
				c.rate3=0
				c.lifton =0
				c.reloc = 0
				c.save()
		pass

	def get_summary(self):
		summary = self.container_set.all().values('container_size').annotate(
			total=Sum('dwell'),
			rate1 =Sum('rate1'),
			rate2 =Sum('rate2'),
			rate3 =Sum('rate3'),
			lifton =Sum('lifton'),
			reloc =Sum('reloc')
			)
		return summary


class Container(models.Model):
	number = models.CharField(max_length=50,blank=False, null=False)
	slug = models.SlugField(unique=True,blank=True, null=True)
	booking  = models.ForeignKey('Booking')
	iso = models.CharField(max_length=10,blank=True, null=True)
	container_type = models.CharField(max_length=10,default='DV')
	container_size = models.CharField(max_length=10,blank=True, null=True ,default='20')
	container_high = models.CharField(max_length=10,blank=True, null=True ,default='8.6')
	in_date  = models.DateTimeField(blank=True, null=True)
	out_date  = models.DateTimeField(blank=True, null=True)
	dwell = models.IntegerField(default=1)
	charge = models.IntegerField(default=0)
	rate1 = models.IntegerField(default=0)
	rate2 = models.IntegerField(default=0)
	rate3 = models.IntegerField(default=0)
	lifton = models.IntegerField(default=0)
	reloc = models.IntegerField(default=0)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.number

	def get_absolute_url(self):
		return reverse('crm:detail', kwargs={'slug':self.slug})

	def lifton_charge(self):
		if not self.booking.vip:
			return 0
		return 1 if self.booking.vip.lifton else 0

	def relocation_charge(self):
		if not self.booking.vip:
			return 0
		return 1 if self.booking.vip.reloc and self.dwell > 7 else 0

	def get_charge(self):
		if self.booking.vip:
			# if self.dwell > self.booking.vip.storage:
			# 	return self.booking.vip.storage- self.booking.vip.no_back_charge
			
			# if (self.dwell <= self.booking.vip.storage) and (self.dwell> self.booking.vip.no_back_charge):
			# 	return  self.dwell - self.booking.vip.no_back_charge

			# Find total final charge (days)
			if self.dwell > self.booking.vip.storage:
				total_charge = self.booking.vip.storage - self.booking.vip.no_back_charge
			else:
				total_charge = self.dwell - self.booking.vip.no_back_charge

			if total_charge<0:
				total_charge=0

			# if total_charge > self.booking.vip.storage :
			# 	total_charge = self.booking.vip.storage - self.dwell

			# Rate Handling
			rate1=0
			rate2=0
			rate3=0
			if self.booking.vip.no_back_charge <= 7:
				if total_charge <=7:
					rate1= total_charge
				elif total_charge > 7 and total_charge <=14 :
					rate1= 7
					rate2= total_charge -7
				else:
					rate1= 7
					rate2= 7
					rate3 = total_charge -14

			if self.booking.vip.no_back_charge > 7 and self.booking.vip.no_back_charge <= 14:
				if total_charge <=7:
					rate2= total_charge
				else :
					rate2= 7
					rate3= total_charge -7

			if self.booking.vip.no_back_charge > 14 :
					rate3 = total_charge

			lifton=0
			if self.booking.vip.lifton:
				lifton = 1

			reloc=0
			if self.booking.vip.reloc and self.dwell>7 :
				reloc = 1 

			return total_charge,rate1,rate2,rate3,lifton,reloc

		return 0

	def update_charge(self):
		self.charge = self.get_charge()[0]
		self.rate1 = self.get_charge()[1]
		self.rate2 = self.get_charge()[2]
		self.rate3 = self.get_charge()[3]
		self.lifton = self.get_charge()[4]
		self.reloc = self.get_charge()[5]
		# if self.booking.vip:
		# 	if self.dwell > self.booking.vip.storage:
		# 		self.charge = self.booking.vip.storage-self.dwell
			
		# 	if (self.dwell <= self.booking.vip.storage) and (self.dwell> self.booking.vip.no_back_charge):
		# 		self.charge =  self.dwell - self.booking.vip.no_back_charge
		# pass

class Charge(models.Model):
	name 			= models.CharField(unique=True,verbose_name ='Charge name',max_length=100)
	status 			= models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date 	= models.DateTimeField(auto_now_add=True)
	modified_date 	= models.DateTimeField(blank=True, null=True,auto_now=True)
	user 			= models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return ('%s' % self.name)

class Extra_Charge(models.Model):
	booking         = models.ForeignKey('Booking',blank=True, null=True)
	container 		= models.ForeignKey('Container',blank=True, null=True)
	charge 			= models.ForeignKey('Charge')
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	remark			= models.TextField()
	qty				= models.IntegerField(default=1)
	status 			= models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date 	= models.DateTimeField(auto_now_add=True)
	modified_date 	= models.DateTimeField(blank=True, null=True,auto_now=True)
	user 			= models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return ('%s - %s' % (self.booking,self.charge))


class Vip(models.Model):
	start_date 		= models.DateTimeField(blank=True, null=True)
	end_date 		=  models.DateTimeField(blank=True, null=True)
	line 			= models.ForeignKey('Line',blank=True, null=True)
	consignee 		= models.ForeignKey('Customer',blank=True, null=True)
	no_back_charge 	= models.IntegerField(default=0)
	storage 		= models.IntegerField(default=0)
	lifton 			= models.BooleanField(default=False)
	reloc 			= models.BooleanField(default=False)
	status 			= models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date 	= models.DateTimeField(auto_now_add=True)
	modified_date 	= models.DateTimeField(blank=True, null=True,auto_now=True)
	user 			= models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return ('%s-%s' % (self.line,self.consignee))


# Slug Hadeling#
def create_slug(model,instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = model.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count()+1)
        return create_slug(model,instance, new_slug=new_slug)
    return slug

def create_number_slug(model,instance, new_slug=None):
    slug = slugify(instance.number)
    if new_slug is not None:
        slug = new_slug
    qs = model.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count()+1)
        return create_slug(model,instance, new_slug=new_slug)
    return slug

def create_text_slug(model,instance, new_slug=None):
    slug = slugify(new_slug)
    qs = model.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count()+1)
        return create_text_slug(model,instance, new_slug=new_slug)
    return slug


# Booking File
def pre_save_bookingfile_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(BookingFile,instance)

# Vessel
def pre_save_vessel_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(Vessel,instance)

# Customer
def pre_save_customer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(Customer,instance)

# Line
def pre_save_line_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(Line,instance)

# Agent
def pre_save_agent_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(Agent,instance)

# BillTo
def pre_save_billto_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(BillTo,instance)

# Booking
def pre_save_booking_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(Booking,instance)
    if not instance.ssr_code:
    	instance.ssr_code = '%s-CRM-0000000' % ('A' if instance.company.name == 'LCMT' else 'B')

# Container
def pre_save_container_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_number_slug(Container,instance)

# Extra Charge
def pre_save_extra_charge_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = '%s-%s' % (instance.booking,instance.container)
		instance.slug = create_text_slug(Extra_Charge,instance,slug)

pre_save.connect(pre_save_bookingfile_receiver, sender=BookingFile)
pre_save.connect(pre_save_agent_receiver, sender=Agent)
pre_save.connect(pre_save_billto_receiver, sender=BillTo)
pre_save.connect(pre_save_booking_receiver, sender=Booking)
pre_save.connect(pre_save_container_receiver, sender=Container)
pre_save.connect(pre_save_customer_receiver, sender=Customer)
pre_save.connect(pre_save_line_receiver, sender=Line)
pre_save.connect(pre_save_vessel_receiver, sender=Vessel)
pre_save.connect(pre_save_extra_charge_receiver, sender=Extra_Charge)