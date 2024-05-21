from django.contrib import admin
from .models import Driver, Vehicle, RunRequest
# Register your models here.

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(RunRequest)