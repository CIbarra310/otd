from django import forms
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

    run_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
    ready_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    need_by_this_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('dashboard')
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('production_title', label=False),
            Field('requester_name', label=False),
            Field('requester_phone', label=False),
            Field('requester_email', label=False),
            Field('requester_department', label=False),
            Field('run_date', css_class='run-request-input', label=False),
            Field('ready_time', css_class='run-request-input', label=False),
            Field('need_by_this_time', css_class='run-request-input', label=False),
            Field('pickup_name', label=False),
            Field('pickup_phone', label=False),
            Field('pickup_address_1', label=False),
            Field('pickup_address_2', label=False),
            Field('pickup_city', label=False),
            Field('pickup_state', label=False),
            Field('pickup_zip', label=False),
            Field('dropoff_name', label=False),
            Field('dropoff_phone', label=False),
            Field('dropoff_address_1', label=False),
            Field('dropoff_address_2', label=False),
            Field('dropoff_city', label=False),
            Field('dropoff_state', label=False),
            Field('dropoff_zip', label=False),
            Field('truck_size', label=False),
            Field('run_details', label=False),
            Field('assigned_driver', label=False),
            Field('purchase_order', label=False),
            Field('vendor_invoice', label=False),
            Submit('submit', 'Submit')
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