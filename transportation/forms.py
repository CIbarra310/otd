from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.utils import timezone
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