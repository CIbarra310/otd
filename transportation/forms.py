from django import forms
from django.forms import Select
from datetime import datetime
from django.urls import reverse_lazy
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div
from .models import RunRequest, Driver
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
            #'production_title',
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
            'dropoff_name',
            'dropoff_phone',
            'dropoff_address_1',
            'dropoff_address_2',
            'dropoff_city',
            'dropoff_state',
            'dropoff_zip',
            'truck_size',
            'run_details',
            'assigned_driver',
            'purchase_order',
            'vendor_invoice',
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
            'occupation_code',
            'rate',
            'grouping',
            'last_4'
        ]