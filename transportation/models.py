from django.db import models
from core.models import Production, Department
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Driver(models.Model):
    production_title = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    driver_email = models.EmailField(_('email address'), null=True, blank=True)
    driver_phone = models.CharField(max_length=15, null=True, blank=True)
    occupation_code = models.CharField(max_length=4, null=True, blank=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    grouping = models.IntegerField(null=True, blank=True)
    last_4 = models.CharField(max_length=6, null=True, blank=True)
    assigned_vehicle = models.ManyToManyField('Vehicle', blank=True, related_name='drivers')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Vehicle(models.Model):
    production_title = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.CharField(max_length=150, null=True)
    vendor_name = models.CharField(max_length=100, null=True)
    vendor_unit_number = models.CharField(max_length=10, null=True)
    internal_unit_number = models.CharField(max_length=20, null=True)
    purchase_order = models.CharField(max_length=10, null=True)
    vehicle_notes = models.TextField(max_length=2000, null=True, blank=True)
    assigned_department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE, related_name='vehicles')
    assigned_driver = models.ManyToManyField(Driver, blank=True, related_name='vehicles')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_type + " " + self.vendor_unit_number

class RunRequest(models.Model):
    # - Assign production to the run
    production_title = models.CharField(max_length=150, null=True)

    # - Run Create Date
    create_date = models.DateField(auto_now_add=True)
    
    # - Requester Information
    requester_name = models.CharField(max_length=100)
    requester_phone = models.CharField(max_length=15)
    requester_email = models.CharField(max_length=255)
    requester_department = models.CharField(max_length=100)
    run_date = models.DateField()
    ready_time = models.TimeField(null=True, blank=True)
    need_by_this_time = models.TimeField(null=True, blank=True)
    run_type = models.CharField(null=True, max_length=50)

    # - Stop 1 Information
    pickup_name = models.CharField(max_length=100)
    pickup_phone = models.CharField(max_length=15, null=True, blank=True)
    pickup_address_1 = models.CharField(max_length=100)
    pickup_address_2 = models.CharField(max_length=100, null=True, blank=True)
    pickup_city = models.CharField(max_length=100)
    pickup_state = models.CharField(max_length=2)
    pickup_zip = models.CharField(max_length=10)
    run_details = models.TextField(max_length=500)

    # - Stop 2 Information
    dropoff_name = models.CharField(max_length=100, blank=True)
    dropoff_phone = models.CharField(max_length=15, blank=True)
    dropoff_address_1 = models.CharField(max_length=100, blank=True)
    dropoff_address_2 = models.CharField(max_length=100, null=True, blank=True)
    dropoff_city = models.CharField(max_length=100, blank=True)
    dropoff_state = models.CharField(max_length=2, blank=True)
    dropoff_zip = models.CharField(max_length=10, blank=True)
    run_details_2 = models.TextField(max_length=500, null=True, blank=True)

    # - Stop 3 Information
    stop_3_name = models.CharField(max_length=100, blank=True)
    stop_3_phone = models.CharField(max_length=15, blank=True)
    stop_3_address_1 = models.CharField(max_length=100, blank=True)
    stop_3_address_2 = models.CharField(max_length=100, null=True, blank=True)
    stop_3_city = models.CharField(max_length=100, blank=True)
    stop_3_state = models.CharField(max_length=2, blank=True)
    stop_3_zip = models.CharField(max_length=10, blank=True)
    run_details_3 = models.TextField(max_length=500, null=True, blank=True)

    # - Stop 4 Information
    stop_4_name = models.CharField(max_length=100, blank=True)
    stop_4_phone = models.CharField(max_length=15, blank=True)
    stop_4_address_1 = models.CharField(max_length=100, blank=True)
    stop_4_address_2 = models.CharField(max_length=100, null=True, blank=True)
    stop_4_city = models.CharField(max_length=100, blank=True)
    stop_4_state = models.CharField(max_length=2, blank=True)
    stop_4_zip = models.CharField(max_length=10, blank=True)
    run_details_4 = models.TextField(max_length=500, null=True, blank=True)

    # - Stop 5 Information
    stop_5_name = models.CharField(max_length=100, blank=True)
    stop_5_phone = models.CharField(max_length=15, blank=True)
    stop_5_address_1 = models.CharField(max_length=100, blank=True)
    stop_5_address_2 = models.CharField(max_length=100, null=True, blank=True)
    stop_5_city = models.CharField(max_length=100, blank=True)
    stop_5_state = models.CharField(max_length=2, blank=True)
    stop_5_zip = models.CharField(max_length=10, blank=True)
    run_details_5 = models.TextField(max_length=500, null=True, blank=True)

    # - Stop 6 Information
    stop_6_name = models.CharField(max_length=100, blank=True)
    stop_6_phone = models.CharField(max_length=15, blank=True)
    stop_6_address_1 = models.CharField(max_length=100, blank=True)
    stop_6_address_2 = models.CharField(max_length=100, null=True, blank=True)
    stop_6_city = models.CharField(max_length=100, blank=True)
    stop_6_state = models.CharField(max_length=2, blank=True)
    stop_6_zip = models.CharField(max_length=10, blank=True)
    run_details_6 = models.TextField(max_length=500, null=True, blank=True)

    # - Run Details
    purchase_order = models.CharField(max_length=20, null=True, blank=True)
    vendor_invoice  = models.CharField(max_length=20, null=True, blank=True)
    run_status = models.CharField(max_length=20, null=True, blank=True)
    truck_size = models.CharField(max_length=50, null=True, blank=True)
    assigned_driver = models.CharField(max_length=100, null=True, blank=True)

    # - Transportation Notes
    transportation_notes = models.TextField(max_length=2000, null=True, blank=True)
    driver_notes = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "Run #" + str(self.id) + " - " + self.requester_department
    