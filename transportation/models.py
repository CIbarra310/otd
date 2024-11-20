from django.db import models
from core.models import Production, Department
from django.utils.translation import gettext_lazy as _
from django.conf import settings  # Import settings to get the custom user model

# Create your models here.
class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    production_title = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    driver_email = models.EmailField(_('email address'), null=True, blank=True)
    driver_birthdate = models.DateField(null=True, blank=True)
    driver_phone = models.CharField(max_length=15, null=True, blank=True)
    occupation_code = models.CharField(max_length=4, null=True, blank=True)
    job_classification = models.CharField(max_length=50, null=True, blank=True)
    driver_hire_date = models.DateField(null=True, blank=True)
    production_status = models.CharField(max_length=50, null=True, blank=True) # On production or off production
    rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    grouping = models.IntegerField(null=True, blank=True)
    local = models.IntegerField(null=True, blank=True)
    last_4 = models.CharField(max_length=6, null=True, blank=True)
    drivers_license_number = models.CharField(max_length=20, null=True, blank=True)
    drivers_license_expiration = models.DateField(null=True, blank=True)
    drivers_license_state = models.CharField(max_length=2, null=True, blank=True)
    drivers_license_class = models.CharField(max_length=2, null=True, blank=True)
    drivers_license_endorsements = models.CharField(max_length=50, null=True, blank=True)
    drivers_license_restrictions = models.CharField(max_length=50, null=True, blank=True)
    medical_card_expiration = models.DateField(null=True, blank=True)
    assigned_truck = models.ManyToManyField('Equipment', related_name='assigned_truck', limit_choices_to={'equipment_type_1': 'truck'})
    assigned_trailer = models.ManyToManyField('Equipment', related_name='assigned_trailer', limit_choices_to={'equipment_type_1': 'trailer'})
    supporting_department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE, related_name='drivers')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class MyCrew(models.Model):
    coordinator_email = models.EmailField(_('email address'), null=True, blank=True)
    my_crew_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Use custom user model
    my_crew_first_name = models.CharField(max_length=150, null=True, blank=True)
    my_crew_last_name = models.CharField(max_length=150, null=True, blank=True)
    my_crew_driver_email = models.EmailField(_('email address'), null=True, blank=True)
    my_crew_driver_birthdate = models.DateField(null=True, blank=True)
    my_crew_driver_phone = models.CharField(max_length=15, null=True, blank=True)
    my_crew_occupation_code = models.CharField(max_length=4, null=True, blank=True)
    my_crew_job_classification = models.CharField(max_length=50, null=True, blank=True)
    my_crew_driver_hire_date = models.DateField(null=True, blank=True)
    my_crew_production_status = models.CharField(max_length=50, null=True, blank=True) # On production or off production
    my_crew_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    my_crew_grouping = models.IntegerField(null=True, blank=True)
    my_crew_local = models.IntegerField(null=True, blank=True)
    my_crew_last_4 = models.CharField(max_length=6, null=True, blank=True)
    my_crew_drivers_license_number = models.CharField(max_length=20, null=True, blank=True)
    my_crew_drivers_license_expiration = models.DateField(null=True, blank=True)
    my_crew_drivers_license_state = models.CharField(max_length=2, null=True, blank=True)
    my_crew_drivers_license_class = models.CharField(max_length=2, null=True, blank=True)
    my_crew_drivers_license_endorsements = models.CharField(max_length=50, null=True, blank=True)
    my_crew_drivers_license_restrictions = models.CharField(max_length=50, null=True, blank=True)
    my_crew_medical_card_expiration = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Equipment(models.Model):
    EQUIPMENT_TYPE_1_CHOICES = [
        ('truck', 'Truck'),
        ('trailer', 'Trailer'),
    ]
    TRUCK_TYPE_CHOICES = [
        ('stakebed', 'Stakebed'),
        ('box_truck', 'Box Truck'),
        ('5_ton', '5-Ton'),
        ('10_ton', '10-Ton'),
        ('tractor', 'Tractor'),
        ('production_van', 'Production Van'),
        ('van', 'Van'),
        # Add more truck types as needed
    ]
    
    TRAILER_TYPE_CHOICES = [
        ('cast_single', 'Cast Single'),
        ('cast_2_room', 'Cast 2-Room'),
        ('cast_3_room', 'Cast 3-Room'),
        ('cast_5_room', 'Cast 5-Room'),
        ('office_trailer', 'Office Trailer'),
        ('wardrobe_trailer', 'Wardrobe Trailer'),
        ('makeup_trailer', 'Makeup Trailer'),
        ('grip_trailer', 'Grip Trailer'),
        ('set_lighting_trailer', 'Set Lighting Trailer'),
        ('equipment_trailer', 'Equipment Trailer'),
        ('honeywagon', 'Honeywagon'),
        ('flatbed', 'Flatbed'),
        # Add more trailer types as needed
    ]
    production_title = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='vehicles')
    equipment_type_1 = models.CharField(max_length=150, choices=EQUIPMENT_TYPE_1_CHOICES , null=True) # truck or trailer
    equipment_type_2 = models.CharField(max_length=150, choices=TRUCK_TYPE_CHOICES, null=True, blank=True) # truck or trailer specific (stakebed, 2 room, etc..)
    trailer_type = models.CharField(max_length=150, choices=TRAILER_TYPE_CHOICES, null=True, blank=True)
    vendor_name = models.CharField(max_length=100, null=True)
    vendor_address_1 = models.CharField(max_length=100, null=True)
    vendor_address_2 = models.CharField(max_length=100, null=True, blank=True)
    vendor_city = models.CharField(max_length=100, null=True)
    vendor_state = models.CharField(max_length=2, null=True)
    vendor_zip = models.CharField(max_length=10, null=True)
    vendor_unit_number = models.CharField(max_length=10, null=True)
    fleet_number = models.CharField(max_length=20, null=True)
    purchase_order = models.CharField(max_length=10, null=True)
    vendor_invoice = models.CharField(max_length=10, null=True)
    equipment_notes = models.TextField(max_length=2000, null=True, blank=True)
    assigned_department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE, related_name='vehicles')
    assigned_driver = models.ManyToManyField(Driver, blank=True, related_name='vehicles')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.equipment_type_1 + " " + self.fleet_number

class PictureCars(models.Model):
    production_title = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='picture_cars')
    year = models.IntegerField(null=True) 
    make = models.CharField(max_length=150, null=True)
    model = models.CharField(max_length=150, null=True)
    vendor_name = models.CharField(max_length=100, null=True)
    vendor_unit_number = models.CharField(max_length=10, null=True)
    scene = models.CharField(max_length=20, null=True)
    purchase_order = models.CharField(max_length=10, null=True)
    picture_car_notes = models.TextField(max_length=2000, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
       return f"{self.year} {self.make} {self.model}"

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
    stop_2_name = models.CharField(max_length=100, blank=True)
    stop_2_phone = models.CharField(max_length=15, blank=True)
    stop_2_address_1 = models.CharField(max_length=100, blank=True)
    stop_2_address_2 = models.CharField(max_length=100, null=True, blank=True)
    stop_2_city = models.CharField(max_length=100, blank=True)
    stop_2_state = models.CharField(max_length=2, blank=True)
    stop_2_zip = models.CharField(max_length=10, blank=True)
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

    # - Drop Off Information
    dropoff_name = models.CharField(max_length=100, blank=True)
    dropoff_phone = models.CharField(max_length=15, blank=True)
    dropoff_address_1 = models.CharField(max_length=100, blank=True)
    dropoff_address_2 = models.CharField(max_length=100, null=True, blank=True)
    dropoff_city = models.CharField(max_length=100, blank=True)
    dropoff_state = models.CharField(max_length=2, blank=True)
    dropoff_zip = models.CharField(max_length=10, blank=True)
    dropoff_details = models.TextField(max_length=500, null=True, blank=True)

    # - Run Details
    purchase_order = models.CharField(max_length=20, null=True, blank=True)
    vendor_invoice  = models.CharField(max_length=20, null=True, blank=True)
    run_status = models.CharField(max_length=20, null=True, blank=True)
    truck_size = models.CharField(max_length=50, null=True, blank=True)
    assigned_driver = models.ManyToManyField('Driver', blank=True)

    # - Transportation Notes
    transportation_notes = models.TextField(max_length=2000, null=True, blank=True)
    driver_notes = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "Run #" + str(self.id) + " - " + self.requester_department

class DriverTimes(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    production_title = models.CharField(max_length=255)
    work_date = models.DateField()
    call_time = models.DecimalField(max_digits=5, decimal_places=2)
    non_deducted_breakfast_in = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wrap_time = models.DecimalField(max_digits=5, decimal_places=2)
    lunch_1_out = models.DecimalField(max_digits=5, decimal_places=2)
    lunch_1_in = models.DecimalField(max_digits=5, decimal_places=2)
    lunch_2_out = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lunch_2_in = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    non_deducted_meal_out = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    non_deducted_meal_in = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meal_penalty_1 = models.IntegerField(null=True, blank=True)
    meal_penalty_2 = models.IntegerField(null=True, blank=True)
    meal_penalty_3 = models.IntegerField(null=True, blank=True)
    times_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.driver} - {self.work_date} - {self.production_title}"    

class DriverTimeComment(models.Model):
    driver_time = models.ForeignKey(DriverTimes, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} created by {self.created_at}"

class DriverDailyRundown(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    date = models.DateField()
    drivers = models.ManyToManyField(Driver)
    equipment = models.ManyToManyField('Equipment')  # Assuming you have an Equipment model
    driver_times = models.ManyToManyField(DriverTimes, blank=True)

    def __str__(self):
        return f"{self.production.production_title} - {self.date}"