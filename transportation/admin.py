from django.contrib import admin
from .models import Driver, Vehicle, RunRequest
# Register your models here.

class DriverAdmin(admin.ModelAdmin):
    list_display = ('production_title', 'first_name', 'last_name', 'driver_email', 'driver_phone', 'grouping')
    search_fields = ('production_title', 'first_name', 'last_name', 'driver_email', 'driver_phone', 'grouping')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('production_title', 'first_name', 'last_name', 'driver_email', 'driver_phone', 'occupation_code', 'rate', 'grouping', 'last_4')
        }),
    )

class RunRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'production_title', 'requester_department', 'run_date', 'pickup_name', 
        'dropoff_name', 'stop_3_name', 'stop_4_name', 'stop_5_name', 'stop_6_name',
    )
    search_fields = ('id', 'requester_name', 'requester_phone', 'requester_email', 'requester_department', 'pickup_name', 'pickup_phone', 'pickup_address_1', 'pickup_address_2', 'pickup_city', 'pickup_state', 'pickup_zip', 'dropoff_name', 'dropoff_phone', 'dropoff_address_1', 'dropoff_address_2', 'dropoff_city', 'dropoff_state')
    list_filter = ('run_date', 'production_title')
    ordering = ('id', 'production_title')
    fieldsets = (
        ('Requester Information', {
            'fields': (
                'production_title', 'requester_name', 'requester_phone', 
                'requester_email', 'requester_department', 'run_date', 'ready_time', 
                'need_by_this_time', 'run_type'
            )
        }),
        ('Stop 1 ', {
            'fields': ('pickup_name', 'pickup_phone', 
                'pickup_address_1', 'pickup_address_2', 'pickup_city', 'pickup_state', 
                'pickup_zip', 'run_details'
            )
        }),
        ('Stop 2 ', {
            'fields': ('dropoff_name', 'dropoff_phone', 
                'dropoff_address_1', 'dropoff_address_2', 'dropoff_city', 'dropoff_state', 
                'dropoff_zip', 'run_details_2',
            )
        }),
        ('Stop 3 ', {
            'fields': ('stop_3_name', 'stop_3_phone', 
                    'stop_3_address_1', 'stop_3_address_2', 'stop_3_city', 'stop_3_state', 
                    'stop_3_zip', 'run_details_3', 
                )
        }),
        ('Stop 4 ', {
            'fields': ('stop_4_name', 'stop_4_phone', 
                'stop_4_address_1', 'stop_4_address_2', 'stop_4_city', 'stop_4_state', 
                'stop_4_zip', 'run_details_4'
            )
        }),
        ('Stop 5', {
            'fields': ('stop_5_name', 'stop_5_phone', 
                'stop_5_address_1', 'stop_5_address_2', 'stop_5_city', 'stop_5_state', 
                'stop_5_zip', 'run_details_5'
            )
        }),
        ('Stop 6', {
            'fields': ('stop_6_name', 'stop_6_phone', 
                'stop_6_address_1', 'stop_6_address_2', 'stop_6_city', 'stop_6_state', 
                'stop_6_zip', 'run_details_6'
                )
        }),
        ('Additional Information', {
            'fields': ('purchase_order', 'vendor_invoice', 
                'run_status', 'truck_size'
                )
        }),
        ('Transportation Information', {
            'fields': ('assigned_driver', 'transportation_notes', 
            'driver_notes')
        }),
    )

admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle)
admin.site.register(RunRequest, RunRequestAdmin)