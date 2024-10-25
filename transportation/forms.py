from django import forms
from django.forms import Select
from datetime import datetime
from django.urls import reverse_lazy
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div
from .models import RunRequest, Driver, Equipment, PictureCars
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

# - Create new run
class NewRunRequest(forms.ModelForm):
    TRUCK_SIZE_CHOICES = [
        ('', 'Select a truck size'),  # Prompt option
        ('Passenger Van', 'Passenger Van'),
        ('Stakebed', 'Stakebed'),
        ('Cube Truck', 'Cube Truck'),
        ('5-Ton', '5-Ton'),
        ('10-Ton', '10-Ton'),
        ('Tractor', 'Tractor'),
        ('Other', 'Other'),
    ]

    truck_size = forms.ChoiceField(choices=TRUCK_SIZE_CHOICES, required=False)
    assigned_driver = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
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
            'run_details',
            'stop_2_name',
            'stop_2_phone',
            'stop_2_address_1',
            'stop_2_address_2',
            'stop_2_city',
            'stop_2_state',
            'stop_2_zip',
            'run_details_2',
            'stop_3_name',
            'stop_3_phone',
            'stop_3_address_1',
            'stop_3_address_2',
            'stop_3_city',
            'stop_3_state',
            'stop_3_zip',
            'run_details_3',
            'stop_4_name',
            'stop_4_phone',
            'stop_4_address_1',
            'stop_4_address_2',
            'stop_4_city',
            'stop_4_state',
            'stop_4_zip',
            'run_details_4',
            'stop_5_name',
            'stop_5_phone',
            'stop_5_address_1',
            'stop_5_address_2',
            'stop_5_city',
            'stop_5_state',
            'stop_5_zip',
            'run_details_5',
            'stop_6_name',
            'stop_6_phone',
            'stop_6_address_1',
            'stop_6_address_2',
            'stop_6_city',
            'stop_6_state',
            'stop_6_zip',
            'run_details_6',
            'dropoff_name',
            'dropoff_phone',
            'dropoff_address_1',
            'dropoff_address_2',
            'dropoff_city',
            'dropoff_state',
            'dropoff_zip',
            'dropoff_details',
            'purchase_order',
            'vendor_invoice',
            'run_status',
            'truck_size',
            'assigned_driver',
            'transportation_notes',
            'driver_notes',
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(NewRunRequest, self).__init__(*args, **kwargs)
        run_instance = kwargs.get('instance')
        if run_instance:
            self.fields['assigned_driver'].queryset = Driver.objects.filter(
                is_active=True,
                production_title=run_instance.production_title
            )

        # Set readonly attribute on specific fields
        self.fields['requester_name'].widget.attrs['readonly'] = True
        self.fields['requester_phone'].widget.attrs['readonly'] = True
        self.fields['requester_email'].widget.attrs['readonly'] = True
        self.fields['requester_department'].widget.attrs['readonly'] = True
        self.fields['run_status'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_show_labels = False 
        self.helper.layout = Layout(
            Field('production_title', css_class='form-control', placeholder='Production Title', label=False),
            Field('requester_name', css_class='form-control', placeholder='Requester Name', label=''),
            Field('requester_phone', css_class='form-control', placeholder='Requester Phone', label=''),
            Field('requester_email', css_class='form-control', placeholder='Requester Email', label=''),
            Field('requester_department', css_class='form-control', placeholder='Requester Department', label=''),
            Field('run_date', css_class='form-control', placeholder='Run Date', label=''),
            Field('ready_time', css_class='form-control', placeholder='Ready Time', label=''),
            Field('need_by_this_time', css_class='form-control', placeholder='Need By This Time', label=''),
            Field('pickup_name', css_class='form-control', placeholder='Pickup Name', label=''),
            Field('pickup_phone', css_class='form-control', placeholder='Pickup Phone', label=''),
            Field('pickup_address_1', css_class='form-control', placeholder='Pickup Address 1', label=''),
            Field('pickup_address_2', css_class='form-control', placeholder='Pickup Address 2', label=''),
            Field('pickup_city', css_class='form-control', placeholder='Pickup City', label=''),
            Field('pickup_state', css_class='form-control', placeholder='Pickup State', label=''),
            Field('pickup_zip', css_class='form-control', placeholder='Pickup Zip', label=''),
            Field('run_details', css_class='form-control', placeholder='Run Details', label=''),
            Field('stop_2_name', css_class='form-control', placeholder='Stop 2 Name', label=''),
            Field('stop_2_phone', css_class='form-control', placeholder='Stop 2 Phone', label=''),
            Field('stop_2_address_1', css_class='form-control', placeholder='Stop 2 Address 1', label=''),
            Field('stop_2_address_2', css_class='form-control', placeholder='Stop 2 Address 2', label=''),
            Field('stop_2_city', css_class='form-control', placeholder='Stop 2 City', label=''),
            Field('stop_2_state', css_class='form-control', placeholder='Stop 2 State', label=''),
            Field('stop_2_zip', css_class='form-control', placeholder='Stop 2 Zip', label=''),
            Field('run_details_2', css_class='form-control', placeholder='Run Details 2', label=''),
            Field('stop_3_name', css_class='form-control', placeholder='Stop 3 Name', label=''),
            Field('stop_3_phone', css_class='form-control', placeholder='Stop 3 Phone', label=''),
            Field('stop_3_address_1', css_class='form-control', placeholder='Stop 3 Address 1', label=''),
            Field('stop_3_address_2', css_class='form-control', placeholder='Stop 3 Address 2', label=''),
            Field('stop_3_city', css_class='form-control', placeholder='Stop 3 City', label=''),
            Field('stop_3_state', css_class='form-control', placeholder='Stop 3 State', label=''),
            Field('stop_3_zip', css_class='form-control', placeholder='Stop 3 Zip', label=''),
            Field('run_details_3', css_class='form-control', placeholder='Run Details 3', label=''),
            Field('stop_4_name', css_class='form-control', placeholder='Stop 4 Name', label=''),
            Field('stop_4_phone', css_class='form-control', placeholder='Stop 4 Phone', label=''),
            Field('stop_4_address_1', css_class='form-control', placeholder='Stop 4 Address 1', label=''),
            Field('stop_4_address_2', css_class='form-control', placeholder='Stop 4 Address 2', label=''),
            Field('stop_4_city', css_class='form-control', placeholder='Stop 4 City', label=''),
            Field('stop_4_state', css_class='form-control', placeholder='Stop 4 State', label=''),
            Field('stop_4_zip', css_class='form-control', placeholder='Stop 4 Zip', label=''),
            Field('run_details_4', css_class='form-control', placeholder='Run Details 4', label=''),
            Field('stop_5_name', css_class='form-control', placeholder='Stop 5 Name', label=''),
            Field('stop_5_phone', css_class='form-control', placeholder='Stop 5 Phone', label=''),
            Field('stop_5_address_1', css_class='form-control', placeholder='Stop 5 Address 1', label=''),
            Field('stop_5_address_2', css_class='form-control', placeholder='Stop 5 Address 2', label=''),
            Field('stop_5_city', css_class='form-control', placeholder='Stop 5 City', label=''),
            Field('stop_5_state', css_class='form-control', placeholder='Stop 5 State', label=''),
            Field('stop_5_zip', css_class='form-control', placeholder='Stop 5 Zip', label=''),
            Field('run_details_5', css_class='form-control', placeholder='Run Details 5', label=''),
            Field('stop_6_name', css_class='form-control', placeholder='Stop 6 Name', label=''),
            Field('stop_6_phone', css_class='form-control', placeholder='Stop 6 Phone', label=''),
            Field('stop_6_address_1', css_class='form-control', placeholder='Stop 6 Address 1', label=''),
            Field('stop_6_address_2', css_class='form-control', placeholder='Stop 6 Address 2', label=''),
            Field('stop_6_city', css_class='form-control', placeholder='Stop 6 City', label=''),
            Field('stop_6_state', css_class='form-control', placeholder='Stop 6 State', label=''),
            Field('stop_6_zip', css_class='form-control', placeholder='Stop 6 Zip', label=''),
            Field('run_details_6', css_class='form-control', placeholder='Run Details 6', label=''),
            Field('dropoff_name', css_class='form-control', placeholder='Dropoff Name', label=''),
            Field('dropoff_phone', css_class='form-control', placeholder='Dropoff Phone', label=''),
            Field('dropoff_address_1', css_class='form-control', placeholder='Dropoff Address 1', label=''),
            Field('dropoff_address_2', css_class='form-control', placeholder='Dropoff Address 2', label=''),
            Field('dropoff_city', css_class='form-control', placeholder='Dropoff City', label=''),
            Field('dropoff_state', css_class='form-control', placeholder='Dropoff State', label=''),
            Field('dropoff_zip', css_class='form-control', placeholder='Dropoff Zip', label=''),
            Field('dropoff_details', css_class='form-control', placeholder='Dropoff Details', label=''),
            Field('purchase_order', css_class='form-control', placeholder='Purchase Order', label=''),
            Field('vendor_invoice', css_class='form-control', placeholder='Vendor Invoice', label=''),
            Field('run_status', css_class='form-control', placeholder='Run Status', label=''),
            Field('truck_size', css_class='form-control', placeholder='Truck Size', label=''),
            Field('assigned_driver', css_class='form-control', placeholder='Assigned Driver', label=''),
            Field('transportation_notes', css_class='form-control', placeholder='Transportation Notes', label=''),
            Field('driver_notes', css_class='form-control', placeholder='Driver Notes', label=''),
        )


# - Create new driver
class NewDriver(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    driver_email = forms.EmailField(required=True)
    driver_phone = forms.CharField(max_length=15, required=True)
    occupation_code = forms.CharField(max_length=4, required=True)
    rate = forms.DecimalField(max_digits=6, decimal_places=2, required=True)
    grouping = forms.IntegerField(required=True)
    last_4 = forms.CharField(max_length=6, required=True)

    class Meta:
        model = Driver
        fields = [
            'first_name',
            'last_name',
            'driver_email',
            'driver_phone',
            'occupation_code',
            'rate',
            'grouping',
            'last_4'
        ]

    def __init__(self, *args, **kwargs):
        super(NewDriver, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Add New Driver',
                'first_name',
                'last_name',
                'driver_email',
                'driver_phone',
                'occupation_code',
                'rate',
                'grouping',
                'last_4',
            ),
            ButtonHolder(
                Submit('submit', 'Save Driver', css_class='btn btn-primary')
            )
        ) 

# - Create new vehicle
class NewEquipment(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'production_title',
            'equipment_type_1',
            'equipment_type_2',
            'vendor_name',
            'vendor_unit_number',
            'fleet_number',
            'purchase_order',
            'equipment_notes',
            'assigned_department',
            'assigned_driver',
            'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super(NewEquipment, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Add New Equipment',
                'production_title',
                'equipment_type_1',
                'equipment_type_2',
                'vendor_name',
                'vendor_unit_number',
                'fleet_number',
                'purchase_order',
                'equipment_notes',
                'assigned_department',
                'assigned_driver',
                'is_active',
            ),
            ButtonHolder(
                Submit('submit', 'Save Equipment', css_class='btn btn-primary')
            )
        )

        # - Create new picture car
class NewPictureCars(forms.ModelForm):
    class Meta:
        model = PictureCars
        fields = [
            'production_title',
            'year',
            'make',
            'model',
            'vendor_name',
            'vendor_unit_number',
            'scene',
            'purchase_order',
            'picture_car_notes',
            'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super(NewPictureCars, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Add New Picture Car',
                'production_title',
                'year',
                'make',
                'model',
                'vendor_name',
                'vendor_unit_number',
                'scene',
                'purchase_order',
                'picture_car_notes',
                'is_active',
            ),
            ButtonHolder(
                Submit('submit', 'Save Picture Car', css_class='btn btn-primary')
            )
        )