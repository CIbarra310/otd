from django import forms
from django.forms.models import inlineformset_factory
from .models import Location, Production, Department, JobTitle, NewUser, PurchaseOrders, Vendor, PurchaseOrderItem

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

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['production_title',
                  'production_type',
                  'production_studio',
                  'production_email',]

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_title']

class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        fields = ['department_title',
                  'job_title']   

class PurchaseOrdersForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrders
        fields = '__all__'

PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrders, 
    PurchaseOrderItem, 
    fields=('description', 'quantity', 'unit_price'),
    extra=3,
    can_delete=True
    )       