from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.utils import timezone
from core.models import Production, Department, JobTitle, NewUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from transportation.models import RunRequest
from core.models import Production

# - Register/Create a user
class CreateUserForm(UserCreationForm):    
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    production_title = forms.ModelChoiceField(
        queryset=Production.objects.filter(is_active=True).order_by('production_title'),
        empty_label="Select Production Title",
        required=False, # Changed from True to False
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.order_by('department_title'),
        empty_label="Select Department"
    )
    
    job_title = forms.ModelChoiceField(
        queryset=JobTitle.objects.order_by('job_title'),
        empty_label="Select Job Title",
        required=False, # Changed from True to False
        widget=forms.Select(attrs={'class': 'form-control d-none'})  # Add 'd-none' class to hide the field
    )
    
    class Meta:
        model = NewUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'production_title', 'department', 'job_title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False  # Make username non-mandatory
        self.fields['username'].widget = forms.HiddenInput()  # Hide the username field
        self.fields['job_title'].widget = forms.HiddenInput()  # Hide the username field
        self.fields['production_title'].widget = forms.HiddenInput()  # Hide the username field

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Set username to email
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.production_title = self.cleaned_data['production_title']
        user.department = self.cleaned_data['department']
        user.job_title = self.cleaned_data['job_title']
        user.is_active = True
        if commit:
            user.save()
        return user

# - Login a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class AddProductionForm(forms.Form):
    production_code = forms.CharField(max_length=6, min_length=6, help_text="Enter the 6-digit production code")
    production_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)