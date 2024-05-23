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
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        # Customize fields independently
        self.helper.layout = Layout(
            Fieldset(
                'Requester Information',
                Field('requester_name', css_class='form-control-lg', placeholder='Full Name'),
                Field('requester_phone', css_class='form-control-lg', placeholder='Phone Number'),
                Field('requester_email', css_class='form-control-lg', placeholder='Email Address'),
                Field('requester_department', css_class='form-control-lg', placeholder='Department'),
                Field('run_date', css_class='form-control-lg', placeholder='YYYY-MM-DD'),
            ),
            Fieldset(
                'Pick Up Information',
                Field('pickup_name', css_class='form-control-lg', placeholder='Pick Up From'),
                Field('pickup_phone', css_class='form-control-lg', placeholder='Pick Up Phone'),
                Field('pickup_address_1', css_class='form-control-lg', placeholder='Address 1'),
                Field('pickup_address_2', css_class='form-control-lg', placeholder='Address 2 (optional)'),
                Div(
                    Field('pickup_city', css_class='form-control-lg', placeholder='City'),
                    Field('pickup_state', css_class='form-control-lg', placeholder='State', wrapper_class='col-lg-2'),
                    Field('pickup_zip', css_class='form-control-lg', placeholder='Zip Code', wrapper_class='col-lg-4'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'Drop Off Information',
                Field('dropoff_name', css_class='form-control-lg', placeholder='Drop Off To'),
                Field('dropoff_phone', css_class='form-control-lg', placeholder='Drop Off Phone'),
                Field('dropoff_address_1', css_class='form-control-lg', placeholder='Address 1'),
                Field('dropoff_address_2', css_class='form-control-lg', placeholder='Address 2 (optional)'),
                Div(
                    Field('dropoff_city', css_class='form-control-lg', placeholder='City'),
                    Field('dropoff_state', css_class='form-control-lg', placeholder='State', wrapper_class='col-lg-2'),
                    Field('dropoff_zip', css_class='form-control-lg', placeholder='Zip Code', wrapper_class='col-lg-4'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'Run Details',
                Field('truck_size', css_class='form-control-lg', placeholder='Truck Size'),
                Field('run_details', css_class='form-control-lg', placeholder='Run Details'),
                Field('assigned_driver', css_class='form-control-lg', placeholder='Assigned Driver'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit Run Request', css_class='btn-primary w-100 p-2 btn-block')
            )
        )