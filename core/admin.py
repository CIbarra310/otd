from django.contrib import admin

from .models import Production, Vendor, Location, Department, JobTitle, NewUser

from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea, TextInput

class UserAdminConfig(UserAdmin):
    search_fields = ('production_title', 'department', 'job_title')
    list_filter = ('production_title', 'department', 'job_title')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'last_name','phone_number', 'production_title', 'department', 'job_title', 'is_staff', 'is_active')
    fieldsets = (
        ('User Information', {'fields': ('email', 'user_name', 'first_name', 'last_name', 'phone_number')}),
        ('Production Information', {'fields': ('production_title', 'department', 'job_title')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name','password1', 'password2', 'phone_number', 'production_title', 'department', 'job_title', 'is_staff', 'is_active')}
         ),
    )


# Register your models here.
admin.site.register(Production)
admin.site.register(Vendor)
admin.site.register(Location)
admin.site.register(Department)
admin.site.register(JobTitle)
admin.site.register(NewUser, UserAdminConfig)