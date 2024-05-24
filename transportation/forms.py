from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div
from .models import RunRequest

# - Create new run
class NewRunRequest(forms.ModelForm):
    class Meta:
        model = RunRequest
        fields = [
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
            'assigned_driver'
        ]
