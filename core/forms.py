from django import forms
from .models import Location, Production, Department, JobTitle, NewUser

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['production_title',
                  'location_name',
                  'location_contact',
                  'location_phone',
                  'location_address_1',
                  'location_address_2',
                  'location_city',
                  'location_state',
                  'location_zip']
        