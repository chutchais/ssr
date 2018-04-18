from django.conf.urls import url
from django.contrib import admin

from . import views
from .views import (BookingFileListView,
					BookingFileDetailView,
					BookingFileCreateView,
					BookingFileProcess,
					BookingFileVip,
					BookingFileDelete,
					BookingListView,
					BookingDetailView,
					BookingVip,BookingResetVip,
					ExtraChargeCreateView,
					ExtraChargeUpdateView,
					ExtraChargeDeleteView,
					BookingUpdateView,
					BookingSendApprove,
					BookingInvoiceUpdateView)

urlpatterns = [ 
	url(r'^$',BookingListView.as_view(),name='home'),
	# url(r'create/$',BookingFileCreateView.as_view(),name='create'),
	# url(r'(?P<slug>[-\w]+)/process$', BookingFileProcess, name='process'),
	# url(r'(?P<slug>[-\w]+)/delete$', BookingFileDelete, name='delete'),
	# url(r'(?^P<slug>[-\w]+)/vip$', BookingFileVip, name='vip'),
	# url(r'(?P<slug>[-\w]+)/$', BookingFileDetailView.as_view(), name='detail'),
	url(r'^extra/(?P<slug>[-\w]+)/$',ExtraChargeUpdateView.as_view(),name='extra-edit'),
	url(r'^extra/(?P<slug>[-\w]+)/delete$',ExtraChargeDeleteView.as_view(),name='extra-delete'),

	url(r'^booking/$', BookingListView.as_view(),name='booking-list'),
	url(r'^booking/(?P<slug>[-\w]+)/$', BookingDetailView.as_view(), name='booking-detail'),
	url(r'^booking/(?P<slug>[-\w]+)/invoice/$', BookingInvoiceUpdateView.as_view(), name='booking-invoice'),
	url(r'^booking/(?P<slug>[-\w]+)/update/$', BookingUpdateView.as_view(), name='booking-update'),
	url(r'^booking/(?P<slug>[-\w]+)/create-extra/$',ExtraChargeCreateView.as_view(),name='extra-create'),
	url(r'^booking/(?P<slug>[-\w]+)/vip$', BookingVip, name='booking-vip'),
	url(r'^booking/(?P<slug>[-\w]+)/reset-vip$', BookingResetVip, name='booking-resetvip'),
	url(r'^booking/(?P<slug>[-\w]+)/send-approve$', BookingSendApprove, name='booking-send-approve'),

	url(r'^file/$', BookingFileListView.as_view(),name='list'),
	url(r'^file/create/$',BookingFileCreateView.as_view(),name='create'),
	url(r'^file/(?P<slug>[-\w]+)/process$', BookingFileProcess, name='process'),
	url(r'^file/(?P<slug>[-\w]+)/delete$', BookingFileDelete, name='delete'),
	url(r'^file/(?P<slug>[-\w]+)/vip$', BookingFileVip, name='vip'),
	url(r'^file/(?P<slug>[-\w]+)/$', BookingFileDetailView.as_view(), name='detail'),
	
]


admin.site.site_header = 'SSR - CRM'