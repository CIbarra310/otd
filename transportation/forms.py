from django import forms
from datetime import datetime
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div
from .models import RunRequest, Driver

# - Create new run
class NewRunRequest(forms.ModelForm):
    TRUCK_SIZE_CHOICES = [
        ('Please Select Vehicle Size', "Please Select Vehicle Size"),
        ('Van', 'Van'),
        ('Stakebed', 'Stakebed'),
        ('Box Truck', 'Box Truck'),
        ('5-Ton', '5-Ton'),
        ('10-Ton', '10-Ton'),
        ('Tractor', 'Tractor'),
    ]

    run_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
    ready_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','min': datetime.now().date()}))
    need_by_this_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','min': datetime.now().date()}))
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
        labels = {
            'production_title': False,
            'requester_name': False,
            'requester_phone': False,
            'requester_email': False,
            'requester_department': False,
            'run_date': False,
            'ready_time': False,
            'need_by_this_time': False,
            'pickup_name': False,
            'pickup_phone': False,
            'pickup_address_1': False,
            'pickup_address_2': False,
            'pickup_city': False,
            'pickup_state': False,
            'pickup_zip': False,
            'dropoff_name': False,
            'dropoff_phone': False,
            'dropoff_address_1': False,
            'dropoff_address_2': False,
            'dropoff_city': False,
            'dropoff_state': False,
            'dropoff_zip': False,
            'truck_size': False,
            'run_details': False,
            'assigned_driver': False,
            'purchase_order': False,
            'vendor_invoice': False,
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requester_name'].disabled = True
        self.fields['requester_phone'].disabled = True
        self.fields['requester_email'].disabled = True
        self.fields['requester_department'].disabled = True
        self.fields['production_title'].disabled = True

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