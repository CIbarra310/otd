from django import forms
from .models import RadioScanner

class RadioForm(forms.ModelForm):
    class Meta:
        model = RadioScanner
        fields = ['barcode',
                  'production',
                  'assigned_employee',
                  'assigned_department',
                  'notes']