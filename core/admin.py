import random
import string
from django.contrib import admin

from .models import Production, Vendor, Location, Department, JobTitle, NewUser

from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea, TextInput

class UserAdminConfig(UserAdmin):
    search_fields = ('productions', 'department', 'job_title')
    list_filter = ('productions', 'department', 'job_title')
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'production_title', 'department', 'job_title', 'is_staff', 'is_active')
    fieldsets = (
        ('User Information', {'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password')}),
        ('Production Information', {'fields': ('productions', 'department', 'job_title',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password', 'phone_number', 'production_title', 'department', 'job_title', 'is_staff', 'is_active')}
         ),
    )

def generate_production_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('production_title', 'code', 'production_studio', 'production_email', 'purchase_order', 'coordinator_name', 'captain_name', 'is_active')
    search_fields = ('production_title', 'production_studio', 'coordinator_name', 'captain_name')
    list_filter = ('is_active', 'production_studio')
    fieldsets = (
        (None, {
            'fields': ('production_title', 'code', 'production_studio', 'production_email', 'purchase_order', 'coordinator_name', 'coordinator_email', 'captain_name', 'captain_email', 'production_notes', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.code:
            obj.code = generate_production_code()
        super().save_model(request, obj, form, change)

class VendorAdmin(admin.ModelAdmin):
    ordering = ('vendor_name',)
    list_display = ('vendor_name', 'vendor_address_1', 'vendor_address_2', 'vendor_city', 'vendor_state', 'vendor_zip', 'vendor_phone')
    search_fields = ('vendor_name', 'vendor_address_1', 'vendor_address_2', 'vendor_city', 'vendor_state', 'vendor_zip', 'vendor_phone')
    list_filter = ('vendor_name', 'vendor_state')
    fieldsets = (
        (None, {
            'fields': ('vendor_name', 'vendor_address_1', 'vendor_address_2', 'vendor_city', 'vendor_state', 'vendor_zip', 'vendor_phone')
        }),
    )

class LocationAdmin(admin.ModelAdmin):
    ordering = ('location_name',)
    list_display = ('location_name', 'location_address_1', 'location_address_2', 'location_city', 'location_state', 'location_zip', 'location_phone')
    search_fields = ('location_name', 'location_address_1','location_address_2', 'location_city', 'location_state', 'location_zip', 'location_phone')
    list_filter = ('location_name', 'location_state')
    fieldsets = (
        (None, {
            'fields': ('production_title','location_name','location_contact', 'location_phone', 'location_address_1', 'location_address_2', 'location_city', 'location_state', 'location_zip')
        }),
    )

class DepartmentAdmin(admin.ModelAdmin):
    ordering = ('department_title',)
    list_display = ('department_title',)
    search_fields = ('department_title',)
    list_filter = ('department_title',)
    fieldsets = (
        (None, {
            'fields': ('department_title',)
        }),
    )

class JobTitleAdmin(admin.ModelAdmin):
    ordering = ('job_title',)
    list_display = ('job_title', 'department_title')
    search_fields = ('job_title', 'department_title')
    list_filter = ('job_title',)
    fieldsets = (
        (None, {
            'fields': ('job_title', 'department_title')
        }),
    )

# Register your models here.
admin.site.register(Production, ProductionAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(JobTitle, JobTitleAdmin)
admin.site.register(NewUser, UserAdminConfig)