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