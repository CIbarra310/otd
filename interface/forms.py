from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.utils import timezone
from core.models import Production, Department, JobTitle
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from transportation.models import RunRequest

# - Register/Create a user
class CreateUserForm(UserCreationForm):    
    email = forms.EmailField()
    user_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    production_title = forms.ModelChoiceField(
        queryset=Production.objects.filter(is_active=True).order_by('production_title'),
        empty_label="Select Production Title"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.order_by('department_title'),
        empty_label="Select Department"
    )
    job_title = forms.ModelChoiceField(
        queryset=JobTitle.objects.order_by('job_title'),
        empty_label="Select Job Title"
    )
    # job_title = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2', 'first_name', 'last_name', 'job_title', 'department', 'production_title']


# - Login a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

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

    def __init__(self, *args, **kwargs):
        super(NewRunRequest, self).__init__(*args, **kwargs)
        self.fields['requester_name'].widget.attrs['disabled'] = True
        self.fields['requester_phone'].widget.attrs['disabled'] = True
        self.fields['requester_email'].widget.attrs['disabled'] = True
        self.fields['requester_department'].widget.attrs['disabled'] = True