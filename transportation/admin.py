from django.contrib import admin
from .models import Driver, Vehicle, RunRequest
# Register your models here.

class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'driver_email', 'driver_phone')
    search_fields = ('first_name', 'last_name', 'driver_email')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'driver_email', 'driver_phone')
        }),
    )

class RunRequestAdmin(admin.ModelAdmin):
    list_display = ('id','production_title', 'requester_department', 'run_date', 'pickup_name', 'pickup_phone', 'pickup_address_1', 'pickup_address_2', 'pickup_city', 'pickup_state', 'pickup_zip', 'dropoff_name', 'dropoff_phone', 'dropoff_address_1', 'dropoff_address_2', 'dropoff_city', 'dropoff_state')
    search_fields = ('requester_name', 'requester_phone', 'requester_email', 'requester_department', 'pickup_name', 'pickup_phone', 'pickup_address_1', 'pickup_address_2', 'pickup_city', 'pickup_state', 'pickup_zip', 'dropoff_name', 'dropoff_phone', 'dropoff_address_1', 'dropoff_address_2', 'dropoff_city', 'dropoff_state')
    list_filter = ('run_date', 'production_title')
    ordering = ('id', 'production_title')
    fieldsets = (
        (None, {
            'fields': ('id', 'production_title', 'requester_department', 'run_date', 'pickup_name', 'pickup_phone', 'pickup_address_1', 'pickup_address_2', 'pickup_city', 'pickup_state', 'pickup_zip', 'dropoff_name', 'dropoff_phone', 'dropoff_address_1', 'dropoff_address_2', 'dropoff_city', 'dropoff_state', 'dropoff_zip')
        }),
    )

admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle)
admin.site.register(RunRequest, RunRequestAdmin)