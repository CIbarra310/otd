from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Driver(models.Model):
    production_title = models.CharField(max_length=150, null=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    driver_email = models.EmailField(_('email address'), null=True)
    occupation_code = models.CharField(max_length=4, null=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    last_4 = models.CharField(max_length=6, null=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Vehicle(models.Model):
    production_title = models.CharField(max_length=150, null=True)
    vehicle_type = models.CharField(max_length=150, null=True)
    vendor_name = models.CharField(max_length=100, null=True)
    vendor_unit_number = models.CharField(max_length=10, null=True)
    internal_unit_number = models.CharField(max_length=20, null=True)
    purchase_order = models.CharField(max_length=10, null=True)
    vehicle_notes = models.TextField(max_length=2000, null=True)
    assigned_driver = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.vehicle_type + " " + self.vendor_unit_number

class RunRequest(models.Model):
    production_title = models.CharField(max_length=150, null=True)
    #Run Create Date
    create_date = models.DateField(auto_now_add=True)
    #Requester Information
    requester_name = models.CharField(max_length=100)
    requester_phone = models.CharField(max_length=15)
    requester_email = models.CharField(max_length=255)
    requester_department = models.CharField(max_length=100)
    run_date = models.DateField()
    ready_time = models.TimeField(null=True, blank=True)
    need_by_this_time = models.TimeField(null=True, blank=True)

    #Pick Up Information
    pickup_name = models.CharField(max_length=100)
    pickup_phone = models.CharField(max_length=15, null=True, blank=True)
    pickup_address_1 = models.CharField(max_length=100)
    pickup_address_2 = models.CharField(max_length=100, null=True, blank=True)
    pickup_city = models.CharField(max_length=100)
    pickup_state = models.CharField(max_length=2)
    pickup_zip = models.CharField(max_length=10)

    #Drop Off Information
    dropoff_name = models.CharField(max_length=100)
    dropoff_phone = models.CharField(max_length=15, blank=True)
    dropoff_address_1 = models.CharField(max_length=100)
    dropoff_address_2 = models.CharField(max_length=100, null=True, blank=True)
    dropoff_city = models.CharField(max_length=100)
    dropoff_state = models.CharField(max_length=2)
    dropoff_zip = models.CharField(max_length=10)

    #Run Details
    purchase_order = models.CharField(max_length=20, null=True, blank=True)
    vendor_invoice  = models.CharField(max_length=20, null=True, blank=True)
    run_status = models.CharField(max_length=20, null=True)
    truck_size = models.CharField(max_length=50, null=True, blank=True)
    run_details = models.TextField(max_length=500)
    assigned_driver = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Run #" + str(self.id) + " - " + self.requester_department
    