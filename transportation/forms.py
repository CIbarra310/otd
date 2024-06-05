from django import forms
from django.forms import Select
from datetime import datetime
from django.urls import reverse_lazy
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div
from .models import RunRequest, Driver
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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

    run_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}),
        label=''  # Remove label
    )
    ready_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label=''
    )
    need_by_this_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label=''
    )
    pickup_name = forms.CharField(
        label=''
    )
    pickup_address_1 = forms.CharField(
        label=''
    )
    pickup_address_2 = forms.CharField(
        label=''
    )
    pickup_city = forms.CharField(
        label=''
    )
    pickup_state = forms.CharField(
        label=''
    )
    pickup_zip = forms.CharField(
        label=''
    )
    run_details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter run details'}),
        label=''  # Remove label
    )
    dropoff_name = forms.CharField(
        label=''
    )
    dropoff_address_1 = forms.CharField(
        label=''
    )
    dropoff_address_2 = forms.CharField(
        label=''
    )
    dropoff_city = forms.CharField(
        label=''
    )
    dropoff_state = forms.CharField(
        label=''
    )
    dropoff_zip = forms.CharField(
        label=''
    )
    purchase_order = forms.CharField(
        label=''
    )
    vendor_invoice = forms.CharField(
        label=''
    )
    truck_size = forms.ChoiceField(
        choices=TRUCK_SIZE_CHOICES,
        widget=Select(attrs={'class': 'form-control'}),
        label=''
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('production_title', label=''),
            Field('requester_name', label='Requester Name'),
            Field('requester_phone', label=''),
            Field('requester_email', label='Email'),
            Field('requester_department', label='Department'),
            Field('run_date', label=''),
            Field('ready_time', label='Ready Time'),
            Field('need_by_this_time', label='Need by Time'),
            Field('pickup_name', label=''),
            Field('pickup_phone', label='Pickup Phone'),
            Field('pickup_address_1', label='Pickup Address 1'),
            Field('pickup_address_2', label='Pickup Address 2'),
            Field('pickup_city', label='City'),
            Field('pickup_state', label='State'),
            Field('pickup_zip', label='Zip Code'),
            Field('dropoff_name', label='Dropoff Name'),
            Field('dropoff_phone', label='Dropoff Phone'),
            Field('dropoff_address_1', label='Dropoff Address 1'),
            Field('dropoff_address_2', label='Dropoff Address 2'),
            Field('dropoff_city', label='City'),
            Field('dropoff_state', label='State'),
            Field('dropoff_zip', label='Zip Code'),
            Field('truck_size', label='Truck Size'),
            Field('run_details', label='Details'),
            Field('assigned_driver', label='Driver'),
            Field('purchase_order', label='PO'),
            Field('vendor_invoice', label='Invoice'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary')
            )
        )


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