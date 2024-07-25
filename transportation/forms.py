from django import forms
from django.forms import Select
from datetime import datetime
from django.urls import reverse_lazy
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div
from .models import RunRequest, Driver, Vehicle
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

# - Create new run
class NewRunRequest(forms.ModelForm):
    TRUCK_SIZE_CHOICES = [
        ('', 'Select a truck size'),  # Prompt option
        ('Passenger Van', 'Passenger Van'),
        ('Stakebed', 'Stakebed'),
        ('Cube Truck', 'Cube Truck'),
        ('5-Ton', '5-Ton'),
        ('10-Ton', '10-Ton'),
    ]

    truck_size = forms.ChoiceField(choices=TRUCK_SIZE_CHOICES)
    
    class Meta:
        model = RunRequest
        fields = [
            'production_title',
            'requester_name',
            'requester_phone',
            'requester_email',
            'requester_department',
            'run_date',
            'ready_time',
            'need_by_this_time',
            'pickup_name',
            'pickup_phone',
            'pickup_address_1',
            'pickup_address_2',
            'pickup_city',
            'pickup_state',
            'pickup_zip',
            'run_details',
            'dropoff_name',
            'dropoff_phone',
            'dropoff_address_1',
            'dropoff_address_2',
            'dropoff_city',
            'dropoff_state',
            'dropoff_zip',
            'run_details_2',
            'stop_3_name',
            'stop_3_phone',
            'stop_3_address_1',
            'stop_3_address_2',
            'stop_3_city',
            'stop_3_state',
            'stop_3_zip',
            'run_details_3',
            'stop_4_name',
            'stop_4_phone',
            'stop_4_address_1',
            'stop_4_address_2',
            'stop_4_city',
            'stop_4_state',
            'stop_4_zip',
            'run_details_4',
            'stop_5_name',
            'stop_5_phone',
            'stop_5_address_1',
            'stop_5_address_2',
            'stop_5_city',
            'stop_5_state',
            'stop_5_zip',
            'run_details_5',
            'stop_6_name',
            'stop_6_phone',
            'stop_6_address_1',
            'stop_6_address_2',
            'stop_6_city',
            'stop_6_state',
            'stop_6_zip',
            'run_details_6',
            'purchase_order',
            'vendor_invoice',
            'run_status',
            'truck_size',
            'assigned_driver',
            'transportation_notes',
            'driver_notes'
        ]

# - Create new driver
class NewDriver(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            'production_title', 
            'first_name',
            'last_name',
            'driver_email',
            'driver_phone',
            'occupation_code',
            'rate',
            'grouping',
            'last_4'
        ]

# - Create new vehicle
class NewVehicle(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'production_title',
            'vehicle_type',
            'vendor_name',
            'vendor_unit_number',
            'internal_unit_number',
            'purchase_order',
            'vehicle_notes',
            'assigned_department',
            'assigned_driver',
            'is_active',
        ]