from django.contrib import admin

from .models import Production, Vendor, Location, Department, JobTitle, NewUser

from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea, TextInput

class UserAdminConfig(UserAdmin):
    search_fields = ('productions', 'department', 'job_title')
    list_filter = ('productions', 'department', 'job_title')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'last_name','phone_number', 'production_title', 'department', 'job_title', 'is_staff', 'is_active')
    fieldsets = (
        ('User Information', {'fields': ('email', 'user_name', 'first_name', 'last_name', 'phone_number')}),
        ('Production Information', {'fields': ('productions', 'department', 'job_title',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name','password1', 'password2', 'phone_number', 'production_title', 'department', 'job_title', 'is_staff', 'is_active')}
         ),
    )

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('production_title', 'production_studio', 'production_email', 'purchase_order', 'coordinator_name', 'captain_name', 'is_active')
    search_fields = ('production_title', 'production_studio', 'coordinator_name', 'captain_name')
    list_filter = ('is_active', 'production_studio')
    fieldsets = (
        (None, {
            'fields': ('production_title', 'production_studio', 'production_email', 'purchase_order', 'coordinator_name', 'coordinator_email', 'captain_name', 'captain_email', 'production_notes', 'is_active')
        }),
    )

# Register your models here.
admin.site.register(Production, ProductionAdmin)
admin.site.register(Vendor)
admin.site.register(Location)
admin.site.register(Department)
admin.site.register(JobTitle)
admin.site.register(NewUser, UserAdminConfig)