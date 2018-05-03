from django.contrib import admin

# Register your models here.
from .models import (Agent,
					Booking,
					BookingFile,
					BillTo,
                    Charge,
					Container,
					Customer,
                    Extra_Charge,
					Line,
					Vessel,
					Vip)

admin.site.register(Agent)
# admin.site.register(Company)
admin.site.register(BookingFile)
admin.site.register(BillTo)
admin.site.register(Charge)
admin.site.register(Container)
admin.site.register(Customer)
admin.site.register(Line)
# admin.site.register(Vessel)
# admin.site.register(Vip)

class VesselAdmin(admin.ModelAdmin):
    search_fields = ['name','code']
    list_filter = []
    list_display = ('__str__','code','description','created_date')
    # list_editable = ('color','move_performa')
    readonly_fields=('created_date',)
    fieldsets = [
        ('Basic Information',{'fields': ['name','code','description','created_date']}),
        ]
admin.site.register(Vessel,VesselAdmin)


class BookingAdmin(admin.ModelAdmin):
    search_fields = ['name','ssr_code','company__name','voy','line__name','agent__name','customer__name','vessel__name']
    list_filter = ['line','agent','customer','vessel']
    list_display = ('__str__','ssr_code','company','voy','line','agent','customer','vessel','vip','draft')
    # list_editable = ('color','move_performa')
    readonly_fields=('created_date',)
    fieldsets = [
        ('Basic Information',{'fields': ['name','ssr_code','company','invoice',
            'cancel_invoice','created_date','draft']}),
        ('Approval',{'fields': ['approved','approve_date']}),
        ('Receive',{'fields': ['received','receive_date']}),
        ]
admin.site.register(Booking,BookingAdmin)

class VipAdmin(admin.ModelAdmin):
    search_fields = ['line','consignee']
    list_filter = ['line','consignee','no_back_charge','storage','lifton','reloc']
    list_display = ('__str__','start_date','end_date','line','consignee','no_back_charge','storage','lifton','reloc')
    # list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['line','consignee']}),
        ('Period of Time',{'fields': [('start_date','end_date')]}),
        ('FEE',{'fields': [('no_back_charge','storage')]}),
        ('Charge',{'fields': [('lifton','reloc')]}),
        ]
admin.site.register(Vip,VipAdmin)


class ExtraChargeAdmin(admin.ModelAdmin):
    search_fields = ['booking','container','charge','remark']
    list_filter = ['charge']
    list_display = ('__str__','booking','container','charge','remark')
    # list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['booking','container','charge','remark','slug']}),
        ]
admin.site.register(Extra_Charge,ExtraChargeAdmin)