import logging
from .forms import LoginForm, CreateUserForm, AddProductionForm
from core.forms import LocationForm, ProductionForm, DepartmentForm, JobTitleForm, PurchaseOrdersForm, PurchaseOrderItemFormSet
from core.models import Production, Vendor, Location, PurchaseOrders, PurchaseOrderItem
from collections import defaultdict
from core.models import Location, Production, Vendor, NewUser, Department
from transportation.forms import NewRunRequest, RunRequest, NewDriver, Driver, NewEquipment, Equipment, NewPictureCars, PictureCars
from transportation.models import DriverTimes, PictureCars, DriverDailyRundown, DriverTimeComment, MyCrew, ProductionHistory
from production.forms import RadioForm
from datetime import datetime, timedelta
from django import forms
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_protect
from core.models import Production, NewUser
import json

logger = logging.getLogger(__name__)

# - Home Page
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # You can use the name of the URL pattern for the dashboard page
    else:
        return render(request, 'interface/index.html')

# - Register a new user
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()  # Normalize email to lowercase
            user.username = user.username.lower()  # Normalize username to lowercase if it's the email
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            print(form.errors)  # Debugging line to print form errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateUserForm()
    
    context = {'form': form}  
    return render(request, 'interface/register.html', context=context) 

# - Login an existing user
@csrf_protect
def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username').lower()
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                 # Retrieve user's first production ID
                current_production_id = user.productions.first().id if user.productions.exists() else None

                # Initialize production_title as None (or handle default case)
                production_title = None

                if current_production_id:
                    try:
                        # Query Production model to get the production title
                        production = Production.objects.get(id=current_production_id)
                        production_title = production.production_title
                    except Production.DoesNotExist:
                        production_title = "Production Not Found"  # Handle case where production is not found

                # Set session variables
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['email'] = user.email
                request.session['phone_number'] = user.phone_number
                request.session['current_production_id'] = current_production_id
                request.session['production_title'] = production_title
                request.session['job_title'] = user.job_title
                request.session['department'] = user.department

                return redirect("login")  # Redirect to dashboard or another view
    
    context = {'form':form}
    return render(request, 'interface/login.html', context=context)

# - Logout a user
def logout(request):
    auth.logout(request)

    # Clear session variables
    request.session.flush()

    messages.success(request, "You have been logged out")
    return redirect("login")

# - Production Admin
@login_required(login_url=login)
def production_admin(request):
    productions = Production.objects.all()

     # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    context = {
        'productions': productions,
        'user_productions': user_productions,    
    }

    return render(request, 'interface/production_admin.html', context = context)

# - Add Production
@login_required(login_url='login')
def add_production(request):
    print("Add Production view accessed.")
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    if request.method == 'POST':
        print("Form submission received.")
        form = AddProductionForm(request.POST)
        if form.is_valid():
            production_code = form.cleaned_data['production_code']
            production_id = form.cleaned_data.get('production_id')
            
            print(f"Form is valid. Production code: {production_code}, Production ID: {production_id}")
            
            if production_id:
                # Step 2: Confirm and add the production
                try:
                    production = Production.objects.get(id=production_id)
                    print(f"Production found: {production.production_title}")
                    
                    # Add production to the current user
                    print(f"User's productions before adding: {request.user.productions.all()}")
                    request.user.productions.add(production)
                    request.user.save()
                    print(f"User's productions after adding: {request.user.productions.all()}")
                    
                    # Add production to the system admin
                    system_admin = NewUser.objects.get(username='admin@ontheday.app')  # Replace 'admin@ontheday.app' with the actual username of the system admin
                    print(f"System admin's productions before adding: {system_admin.productions.all()}")
                    system_admin.productions.add(production)
                    system_admin.save()
                    print(f"System admin's productions after adding: {system_admin.productions.all()}")

                    # Set session data
                    request.session['production_title'] = production.production_title
                    request.session['production_id'] = production.id
                    print(f"Session data set: production_title={request.session['production_title']}, production_id={request.session['production_id']}")

                    messages.success(request, f'Production {production.production_title} added successfully.')
                    print(f"Production {production.production_title} added successfully to user {request.user.username} and system admin.")
                    return redirect('dashboard')
                except Production.DoesNotExist:
                    messages.error(request, 'Invalid production ID.')
                    print("Invalid production ID.")
                except NewUser.DoesNotExist:
                    messages.error(request, 'System admin user does not exist.')
                    print("System admin user does not exist.")
            else:
                # Step 1: Search for the production
                try:
                    production = Production.objects.get(code=production_code)
                    form = AddProductionForm(initial={'production_code': production_code, 'production_id': production.id})
                    print(f"Production found: {production.production_title}")
                    return render(request, 'interface/add_production.html', {'form': form, 'production': production, 'user_productions': user_productions})
                except Production.DoesNotExist:
                    messages.error(request, 'Invalid production code.')
                    print("Invalid production code.")
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = AddProductionForm()

    context = {
        'form': form,
        'user_productions': user_productions,
    }
    return render(request, 'interface/add_production.html', context=context)

# - Location Admin
@login_required(login_url=login)
def location_admin(request):
    locations = Location.objects.all()

     # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

     # Filter runs by production_title in session
    production_title_in_session = request.session.get('production_title')
    if production_title_in_session:
        locations = locations.filter(production_title=production_title_in_session)


    context = {
        'locations': locations,
        'user_productions': user_productions,    
    }

    return render(request, 'interface/location_admin.html', context = context)

# - Add Location
@login_required(login_url='login')
def add_location(request):

    if request.method == "POST":
        location = Location(request.POST)
        if location.is_valid():
            location.save()
            return redirect("location_admin")
        else:
            messages.error(request, "There was an error with your submission. Please check the form for errors.")

    location = Location()

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    context = {
        'location': location,
        'user_productions': user_productions,
    }

    return render(request, 'interface/add_location.html', context = context)

# - View Location
@login_required(login_url='login')
def view_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    return render(request, 'interface/location.html', {'location': location})

# - User Admin
@login_required(login_url=login)
def user_admin(request):
    users = NewUser.objects.all()

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    context = {
        'users': users,
        'user_productions': user_productions,
    }

    return render(request, 'interface/user_admin.html', context = context)

@login_required(login_url='login')  # Ensure 'login' is the correct URL name
def dashboard(request):
     # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)[:5]

    # Check if the user is a driver
    is_driver = Driver.objects.filter(user=user).exists()

    # Initialize runs as an empty queryset
    runs = RunRequest.objects.none()

    # Filter runs by production_title in session
    production_title_in_session = request.session.get('production_title')
    department_in_session = request.session.get('department')
    if production_title_in_session:
        if department_in_session == "Admin" or department_in_session == "Production" or department_in_session == "Transportation":
            runs = RunRequest.objects.filter(production_title=production_title_in_session).order_by('run_date')
        else:
            runs = RunRequest.objects.filter(production_title=production_title_in_session, requester_department=department_in_session).order_by('run_date')
    # Separate and limit "Completed" and "Open" runs
    completed_runs = runs.filter(run_status="Completed")[:5]
    open_runs = runs.filter(run_status__in=["Open", "In Progress"])[:5]

    # Get the current date
    current_date = timezone.now().date()

    # Pass the objects to the template context
    context = {
        'runs': runs,
        'completed_runs': completed_runs,
        'open_runs': open_runs,
        'user_productions': user_productions,
        'is_driver': is_driver,
    }
    return render(request, 'interface/dashboard.html', context=context)

# - Driver roster page
@login_required(login_url='login')
def driver_roster(request):
    drivers = Driver.objects.all()

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Filter drivers by production_title in session
    production_title_in_session = request.session.get('production_title')
    if production_title_in_session:
        drivers = drivers.filter(production_title=production_title_in_session)

    # Pass the objects
    context = {
        'drivers': drivers,
        'user_productions': user_productions,
    }
    return render(request, 'interface/driver_roster.html', context=context)

# - Add Driver
@login_required(login_url='login')
def add_driver(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)
    departments = Department.objects.all()

    # Retrieve production_title from the session
    production_title = request.session.get('production_title')
    if production_title:
        trucks = Equipment.objects.filter(
            equipment_type_1='truck',
            production_title__production_title=production_title,
            assigned_driver__isnull=True  # Filter out trucks that are assigned to other drivers
        )
        trailers = Equipment.objects.filter(
            equipment_type_1='trailer',
            production_title__production_title=production_title,
            assigned_driver__isnull=True  # Filter out trailers that are assigned to other drivers
        )
    else:
        trucks = Equipment.objects.filter(equipment_type_1='truck', assigned_driver__isnull=True)
        trailers = Equipment.objects.filter(equipment_type_1='trailer', assigned_driver__isnull=True)

    if request.method == 'POST':
        form = NewDriver(request.POST)
        if form.is_valid():
            try:
                # Use driver_email to find the existing user
                email = form.cleaned_data['driver_email']
                user = NewUser.objects.filter(email=email).first()
                if not user:
                    return render(request, 'interface/add_driver.html', {'form': form, 'error': 'No user with this email exists.', 'departments': departments, 'trucks': trucks, 'trailers': trailers})

                if not production_title:
                    return render(request, 'interface/add_driver.html', {'form': form, 'error': 'Production title is missing from session.', 'departments': departments, 'trucks': trucks, 'trailers': trailers})

                # Create the Driver instance
                driver = Driver(
                    user=user,
                    production_title=production_title,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    driver_email=form.cleaned_data['driver_email'],
                    driver_phone=form.cleaned_data['driver_phone'],
                    occupation_code=form.cleaned_data['occupation_code'],
                    # Add other fields as necessary
                )
                driver.save()

                return redirect('driver_roster')  # Redirect to the driver roster page after adding the driver

            except Exception as e:
                return render(request, 'interface/add_driver.html', {'form': form, 'error': str(e), 'departments': departments, 'trucks': trucks, 'trailers': trailers})

    else:
        form = NewDriver()

    context = {
        'form': form,
        'user_productions': user_productions,
        'departments': departments,
        'trucks': trucks,
        'trailers': trailers,
    }
    return render(request, 'interface/add_driver.html', context)

@login_required(login_url='login')
def my_crew(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)
    email = request.session.get('email')

    # Fetch all MyCrew objects for the logged-in user
    my_crews = MyCrew.objects.filter(coordinator_email=email)

    context = {
        'user_productions': user_productions,
        'my_crews': my_crews,
    }
    return render(request, 'interface/my_crew.html', context)


@login_required(login_url='login')
def add_favorite(request, driver_id):
    try:
        driver = get_object_or_404(Driver, id=driver_id)
        coordinator_email = request.user.email
        production_title = request.session.get('production_title')
        
        # Ensure the production exists
        production = get_object_or_404(Production, production_title=production_title)
        
        # Get or create a MyCrew object for the logged-in user
        my_crew, created = MyCrew.objects.get_or_create(
            my_crew_user=request.user,
            defaults={'coordinator_email': coordinator_email}
        )

        # Update the MyCrew object with the driver's user information
        my_crew.coordinator_email = coordinator_email
        my_crew.my_crew_user = driver.user
        my_crew.my_crew_first_name = driver.first_name
        my_crew.my_crew_last_name = driver.last_name
        my_crew.my_crew_driver_email = driver.driver_email
        my_crew.my_crew_driver_birthdate = driver.driver_birthdate
        my_crew.my_crew_driver_phone = driver.driver_phone
        my_crew.my_crew_occupation_code = driver.occupation_code
        my_crew.my_crew_job_classification = driver.job_classification
        my_crew.my_crew_production_status = driver.production_status
        my_crew.my_crew_rate = driver.rate
        my_crew.my_crew_grouping = driver.grouping
        my_crew.my_crew_local = driver.local
        my_crew.my_crew_last_4 = driver.last_4
        my_crew.my_crew_drivers_license_number = driver.drivers_license_number
        my_crew.my_crew_drivers_license_expiration = driver.drivers_license_expiration
        my_crew.my_crew_drivers_license_state = driver.drivers_license_state
        my_crew.my_crew_drivers_license_class = driver.drivers_license_class
        my_crew.my_crew_drivers_license_endorsements = driver.drivers_license_endorsements
        my_crew.my_crew_drivers_license_restrictions = driver.drivers_license_restrictions
        my_crew.my_crew_medical_card_expiration = driver.medical_card_expiration
        my_crew.my_crew_production_history.add(production)
        my_crew.save()

        return redirect('driver_roster')
    except IntegrityError as e:
        return HttpResponse(f"IntegrityError: {e}")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


@login_required(login_url='login')
def remove_favorite(request, crew_member_id):
    try:
        # Get the MyCrew object for the logged-in user and the specified crew member
        my_crew = get_object_or_404(MyCrew, id=crew_member_id)
        
        # Delete the MyCrew entry
        my_crew.delete()
        
        return redirect('my_crew')
    except Exception as e:
        return HttpResponse(f"Error: {e}")

@login_required(login_url='login')
def crew_member_detail(request, crew_member_id):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    crew_member = get_object_or_404(MyCrew, id=crew_member_id)
    context = {
        'crew_member': crew_member,
        'user_productions': user_productions,
    }
    return render(request, 'interface/crew_member_detail.html', context)

@login_required(login_url='login')
def update_crew_member(request, crew_member_id):
    crew_member = get_object_or_404(MyCrew, id=crew_member_id)
    
    if request.method == 'POST':
        crew_member.my_crew_first_name = request.POST.get('first_name')
        crew_member.my_crew_last_name = request.POST.get('last_name')
        crew_member.my_crew_driver_email = request.POST.get('email')
        crew_member.my_crew_driver_phone = request.POST.get('phone')
        crew_member.my_crew_grouping = request.POST.get('grouping')
        crew_member.my_crew_last_4 = request.POST.get('last_4')
        crew_member.my_crew_drivers_license_number = request.POST.get('drivers_license_number')
        crew_member.my_crew_drivers_license_expiration = request.POST.get('drivers_license_expiration')
        crew_member.my_crew_drivers_license_state = request.POST.get('drivers_license_state')
        crew_member.my_crew_drivers_license_class = request.POST.get('drivers_license_class')
        crew_member.my_crew_drivers_license_endorsements = request.POST.get('drivers_license_endorsements')
        crew_member.my_crew_drivers_license_restrictions = request.POST.get('drivers_license_restrictions')
        crew_member.my_crew_medical_card_expiration = request.POST.get('medical_card_expiration')
        crew_member.save()
        
        return redirect('crew_member_detail', crew_member_id=crew_member.id)
    
    context = {
        'crew_member': crew_member,
    }
    return render(request, 'interface/crew_member_detail.html', context)


@login_required(login_url='login')
def add_to_current_production(request, crew_member_id):
    crew_member = get_object_or_404(MyCrew, id=crew_member_id)
    current_production_id = request.session.get('current_production_id')
    
    # Ensure the production exists
    production = get_object_or_404(Production, id=current_production_id)
    
    # Create or update the Driver instance
    driver, created = Driver.objects.get_or_create(
        user=crew_member.my_crew_user,
        defaults={
            'first_name': crew_member.my_crew_first_name,
            'last_name': crew_member.my_crew_last_name,
            'driver_email': crew_member.my_crew_driver_email,
            'driver_phone': crew_member.my_crew_driver_phone,
            'grouping': crew_member.my_crew_grouping,
            'last_4': crew_member.my_crew_last_4,
            'drivers_license_number': crew_member.my_crew_drivers_license_number,
            'drivers_license_expiration': crew_member.my_crew_drivers_license_expiration,
            'drivers_license_state': crew_member.my_crew_drivers_license_state,
            'drivers_license_class': crew_member.my_crew_drivers_license_class,
            'drivers_license_endorsements': crew_member.my_crew_drivers_license_endorsements,
            'drivers_license_restrictions': crew_member.my_crew_drivers_license_restrictions,
            'medical_card_expiration': crew_member.my_crew_medical_card_expiration,
            'production_title': production.production_title,
        }
    )

    if not created:
        driver.first_name = crew_member.my_crew_first_name
        driver.last_name = crew_member.my_crew_last_name
        driver.driver_email = crew_member.my_crew_driver_email
        driver.driver_phone = crew_member.my_crew_driver_phone
        driver.grouping = crew_member.my_crew_grouping
        driver.last_4 = crew_member.my_crew_last_4
        driver.drivers_license_number = crew_member.my_crew_drivers_license_number
        driver.drivers_license_expiration = crew_member.my_crew_drivers_license_expiration
        driver.drivers_license_state = crew_member.my_crew_drivers_license_state
        driver.drivers_license_class = crew_member.my_crew_drivers_license_class
        driver.drivers_license_endorsements = crew_member.my_crew_drivers_license_endorsements
        driver.drivers_license_restrictions = crew_member.my_crew_drivers_license_restrictions
        driver.medical_card_expiration = crew_member.my_crew_medical_card_expiration
        driver.production_title = production.production_title
        driver.save()

    return redirect('my_crew')


# - Activate Driver
@login_required(login_url='login')
def activate_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    driver.is_active = True
    driver.save()
    return redirect('driver_roster')

# - Deactivate Driver
@login_required(login_url='login')
def deactivate_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    driver.is_active = False
    driver.save()
    return redirect('driver_roster')

# - Driver Rundown
@login_required(login_url='login')
def driver_rundown(request):
	
    return render(request, 'interface/driver_rundown.html')

# - View Driver
@login_required(login_url='login')
def view_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    departments = Department.objects.all()

    # Retrieve production_title from the session
    production_title = request.session.get('production_title')
    if production_title:
        trucks = Equipment.objects.filter(
            equipment_type_1='truck',
            production_title__production_title=production_title,
            assigned_driver__isnull=True  # Filter out trucks that are assigned to other drivers
        )
        trailers = Equipment.objects.filter(
            equipment_type_1='trailer',
            production_title__production_title=production_title,
            assigned_driver__isnull=True  # Filter out trailers that are assigned to other drivers
        )
    else:
        trucks = Equipment.objects.filter(equipment_type_1='truck', assigned_driver__isnull=True)
        trailers = Equipment.objects.filter(equipment_type_1='trailer', assigned_driver__isnull=True)

    # Fetch assigned trucks and trailers for the driver
    assigned_trucks = driver.assigned_truck.all()
    assigned_trailers = driver.assigned_trailer.all()

    context = {
        'driver': driver,
        'trucks': trucks,
        'trailers': trailers,
        'assigned_trucks': assigned_trucks,
        'assigned_trailers': assigned_trailers,
        'user_productions': user_productions,
    }
    return render(request, 'interface/driver.html', context)

# - Driver Times
@login_required(login_url='login')
def driver_times(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Check if the user is a driver
    is_driver = Driver.objects.filter(user=user).exists()
    
    if request.method == 'POST':

        # Retrieve form data
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        driver_name = f"{first_name} {last_name}" if first_name and last_name else None
        work_date = request.POST.get('work_date')
        call_time = float(request.POST.get('call_time'))
        non_deducted_breakfast_in = request.POST.get('non_deducted_breakfast_in') or 0
        wrap_time = float(request.POST.get('wrap_time'))
        lunch_1_out = float(request.POST.get('lunch_1_out'))
        lunch_1_in = float(request.POST.get('lunch_1_in'))
        non_deducted_meal_out = request.POST.get('non_deducted_meal_out') or 0
        non_deducted_meal_in = request.POST.get('non_deducted_meal_in') or 0
        lunch_2_out = request.POST.get('lunch_2_out') or 0
        lunch_2_in = request.POST.get('lunch_2_in') or 0
        notes = request.POST.get('notes')

        # Convert lunch_2_out and lunch_2_in to float if they are provided, otherwise set to 0
        lunch_2_out = float(lunch_2_out) if lunch_2_out else 0
        lunch_2_in = float(lunch_2_in) if lunch_2_in else 0

        # Calculate total hours
        total_hours = wrap_time - call_time - ((lunch_1_in - lunch_1_out) + (lunch_2_in - lunch_2_out))

         # Calculate meal penalty 1
        if non_deducted_breakfast_in:
            time_from_start = lunch_1_out - float(non_deducted_breakfast_in)
        else:
            time_from_start = lunch_1_out - call_time

        meal_penalty_1 = max(0, (time_from_start - 6.0) // 0.5)

         # Calculate meal penalty 2
        if non_deducted_meal_out:
            time_from_lunch_1 = float(non_deducted_meal_out) - lunch_1_in
        elif lunch_2_out:
            time_from_lunch_1 = lunch_2_out - lunch_1_in
        else:
            time_from_lunch_1 = wrap_time - lunch_1_in

        meal_penalty_2 = max(0, (time_from_lunch_1 - 6.0) // 0.5)

        # Calculate meal penalty 3
        if non_deducted_meal_in:
            time_from_last_meal = wrap_time - float(non_deducted_meal_in)
        else:
            time_from_last_meal = wrap_time - lunch_2_in

        meal_penalty_3 = max(0, (time_from_last_meal - 6.0) // 0.5)

        # Store the form data in the session
        request.session['work_date'] = work_date
        request.session['call_time'] = call_time
        request.session['non_deducted_breakfast_in'] = non_deducted_breakfast_in
        request.session['wrap_time'] = wrap_time
        request.session['lunch_1_out'] = lunch_1_out
        request.session['lunch_1_in'] = lunch_1_in
        request.session['non_deducted_meal_out'] = non_deducted_meal_out
        request.session['non_deducted_meal_in'] = non_deducted_meal_in
        request.session['lunch_2_out'] = lunch_2_out
        request.session['lunch_2_in'] = lunch_2_in
        request.session['notes'] = notes
        request.session['total_hours'] = total_hours
        request.session['meal_penalty_1'] = meal_penalty_1
        request.session['meal_penalty_2'] = meal_penalty_2
        request.session['meal_penalty_3'] = meal_penalty_3

        # Redirect to the confirmation page
        return redirect('driver_times_confirmation')

    context = {
        'user_productions': user_productions,
        'is_driver': is_driver,
    }
    return render(request, 'interface/driver_times.html', context)

@login_required(login_url='login')
def driver_times_confirmation(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Check if the user is a driver
    is_driver = Driver.objects.filter(user=user).exists()

    context = {
        'work_date': request.session.get('work_date'),
        'call_time': request.session.get('call_time'),
        'non_deducted_breakfast_in': request.session.get('non_deducted_breakfast_in'),
        'wrap_time': request.session.get('wrap_time'),
        'lunch_1_out': request.session.get('lunch_1_out'),
        'lunch_1_in': request.session.get('lunch_1_in'),
        'non_deducted_meal_out': request.session.get('non_deducted_meal_out'),
        'non_deducted_meal_in': request.session.get('non_deducted_meal_in'),
        'lunch_2_out': request.session.get('lunch_2_out'),
        'lunch_2_in': request.session.get('lunch_2_in'),
        'notes': request.session.get('notes'),
        'total_hours': request.session.get('total_hours'),
        'user_productions': user_productions,
        'meal_penalty_1': request.session.get('meal_penalty_1'),
        'meal_penalty_2': request.session.get('meal_penalty_2'),
        'meal_penalty_3': request.session.get('meal_penalty_3'),
        'is_driver': is_driver,
    }
    return render(request, 'interface/driver_times_confirmation.html', context)

@login_required(login_url='login')
def driver_times_submit(request):
    if request.method == 'POST':
        # Retrieve form data from the session
        user = request.user
        driver = Driver.objects.get(user=user)
        production_title = request.session.get('production_title')
        work_date = request.session.get('work_date')
        call_time = request.session.get('call_time')
        non_deducted_breakfast_in = request.session.get('non_deducted_breakfast_in')
        wrap_time = request.session.get('wrap_time')
        lunch_1_out = request.session.get('lunch_1_out')
        lunch_1_in = request.session.get('lunch_1_in')
        non_deducted_meal_out = request.session.get('non_deducted_meal_out')
        non_deducted_meal_in = request.session.get('non_deducted_meal_in')
        lunch_2_out = request.session.get('lunch_2_out')
        lunch_2_in = request.session.get('lunch_2_in')
        notes = request.session.get('notes')
        total_hours = request.session.get('total_hours')
        meal_penalty_1 = request.session.get('meal_penalty_1')
        meal_penalty_2 = request.session.get('meal_penalty_2')
        meal_penalty_3 = request.session.get('meal_penalty_3')

        # Save the data to the database
        DriverTimes.objects.create(
            driver=driver,
            production_title=production_title,
            work_date=work_date,
            call_time=call_time,
            non_deducted_breakfast_in=non_deducted_breakfast_in,
            wrap_time=wrap_time,
            lunch_1_out=lunch_1_out,
            lunch_1_in=lunch_1_in,
            non_deducted_meal_out=non_deducted_meal_out,
            non_deducted_meal_in=non_deducted_meal_in,
            lunch_2_out=lunch_2_out,
            lunch_2_in=lunch_2_in,
            notes=notes,
            total_hours=total_hours,
            meal_penalty_1=meal_penalty_1,
            meal_penalty_2=meal_penalty_2,
            meal_penalty_3=meal_penalty_3,
        )

        # Clear the session data
        request.session.pop('work_date', None)
        request.session.pop('call_time', None)
        request.session.pop('non_deducted_breakfast_in', None)
        request.session.pop('wrap_time', None)
        request.session.pop('lunch_1_out', None)
        request.session.pop('lunch_1_in', None)
        request.session.pop('non_deducted_meal_out', None)
        request.session.pop('non_deducted_meal_in', None)
        request.session.pop('lunch_2_out', None)
        request.session.pop('lunch_2_in', None)
        request.session.pop('notes', None)
        request.session.pop('total_hours', None)
        request.session.pop('meal_penalty_1', None)
        request.session.pop('meal_penalty_2', None)
        request.session.pop('meal_penalty_3', None)

        return redirect('driver_times_success')
    return redirect('driver_times')

@login_required(login_url='login')
def driver_times_success(request):
    return render(request, 'interface/driver_times_success.html')

# - View a list of drivers and their times by date
@login_required(login_url='login')
def driver_times_view(request):
     # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Filter driver times by production_title in session
    production_title_in_session = request.session.get('production_title')
    yesterday = datetime.today() - timedelta(days=1)
    date_string = request.GET.get('date', yesterday.strftime('%Y-%m-%d'))
    date = datetime.strptime(date_string, '%Y-%m-%d').date()

    if production_title_in_session:
        driver_times = DriverTimes.objects.filter(production_title=production_title_in_session, work_date=date)
        active_drivers = Driver.objects.filter(is_active=True, production_title=production_title_in_session)
    else:
        driver_times = DriverTimes.objects.filter(work_date=date)
        active_drivers = Driver.objects.filter(is_active=True)

    # Get the list of drivers who do not have a driver time entry
    drivers_with_times = driver_times.values_list('driver', flat=True)
    drivers_without_times = active_drivers.exclude(id__in=drivers_with_times)

    context = {
        'driver_times': driver_times,
        'user_productions': user_productions,
        'date': date_string,
        'drivers_without_times': drivers_without_times,
    }
    return render(request, 'interface/driver_times_view.html', context)

@login_required(login_url='login')
def driver_weekly_times_view(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Get the current date or the date from the query parameter
    date_string = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
    print(f"Received date string: {date_string}")
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        try:
            date = datetime.strptime(date_string, '%b. %d, %Y').date()
        except ValueError:
            date = datetime.today().date()
    print(f"Parsed date: {date}")

    # Calculate the start and end of the week (Sunday to Saturday)
    start_of_week = date - timedelta(days=date.weekday() + 1) if date.weekday() != 6 else date
    end_of_week = start_of_week + timedelta(days=6)
    print(f"Start of week: {start_of_week}, End of week: {end_of_week}")

    # Filter driver times for the selected week
    driver_times = DriverTimes.objects.filter(driver=driver, work_date__range=[start_of_week, end_of_week]).order_by('created_at')

    # Calculate previous and next week dates
    previous_week = start_of_week - timedelta(days=7)
    next_week = start_of_week + timedelta(days=7)
    print(f"Previous week: {previous_week}, Next week: {next_week}")

    context = {
        'driver': driver,
        'driver_times': driver_times,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'previous_week': previous_week.strftime('%Y-%m-%d'),
        'next_week': next_week.strftime('%Y-%m-%d'),
        'user_productions': user_productions,
    }
    return render(request, 'interface/driver_weekly_times_view.html', context)

# - Driver time details (view details of an individual driver's times)
def driver_time_detail(request, id):
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)  
    driver_time = get_object_or_404(DriverTimes, id=id)
    
    # Get the dot admin email from the production associated with the driver time
    production = get_object_or_404(Production, production_title=driver_time.production_title)
    dot_admin_email = production.dot_admin_email
    
    if request.method == 'POST':
        action = request.POST.get('action')
        subject = f'Confirmation of Times for {driver_time.work_date}'
        if action == 'accept':
            body = f"""
            Your times have been accepted.

            Call Time: {driver_time.call_time}
            Non-Deducted Breakfast In: {driver_time.non_deducted_breakfast_in}
            Lunch 1 Out: {driver_time.lunch_1_out}
            Lunch 1 In: {driver_time.lunch_1_in}
            Lunch 2 Out: {driver_time.lunch_2_out}
            Lunch 2 In: {driver_time.lunch_2_in}
            Non-Deducted Meal Out: {driver_time.non_deducted_meal_out}
            Non-Deducted Meal In: {driver_time.non_deducted_meal_in}
            Wrap Time: {driver_time.wrap_time}
            
            Please ensure your timecard is accurate and updated.
            """
            driver_time.times_status = 'Accepted'
            print("Times accepted")
        elif action == 'request_changes':
            body = f"""
            
            Your times have been reviewed and changes are requested. Please partner with the DOT Admin or Transportation Coordinator.

            """
            driver_time.times_status = 'Changes Requested'
            print("Changes requested")
        elif action == 'reject':
            body = f"""
            
            Your times have been rejected for the following reason: 

            """
            driver_time.times_status = 'Rejected'
            print(f"{production} {dot_admin_email} {driver_time.driver.driver_email}")
        
        # Save the updated status
        driver_time.save()

        # Add a new comment if provided
        comment_text = request.POST.get('comment')
        if comment_text:
            DriverTimeComment.objects.create(driver_time=driver_time, user=user, comment=comment_text)
            body += f"\n\n{user.first_name} {user.last_name}: {comment_text}"

        # Send an email to the driver
        recipient_list = [driver_time.driver.driver_email]
        email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list, reply_to=[dot_admin_email])
        email.send(fail_silently=False)
        return redirect('driver_times_view')  # Redirect to a success page after sending the email

    context = {
        'driver_time': driver_time,
        'user_productions': user_productions,
        'comments': driver_time.comments.all(),
    }

    return render(request, 'interface/driver_time_detail.html', context=context)

# - Driver times history for drivers
@login_required(login_url='login')
def driver_times_history(request):
    user = get_object_or_404(NewUser, id=request.user.id)
    driver = get_object_or_404(Driver, user=user)
    user_productions = user.productions.filter(is_active=True)

    # Check if the user is a driver
    is_driver = Driver.objects.filter(user=user).exists()

    # Get the production title from the session for the filter
    production_title = request.session.get('production_title')

    # Filter the driver times by the selected date range and user's productions
    driver_times = DriverTimes.objects.filter(
        driver=driver,
        production_title=production_title,
    )

    context = {
        'driver_times': driver_times,
        'user_productions': user_productions,
        'production_title': production_title,
        'is_driver': is_driver,
    }
    return render(request, 'interface/driver_times_history.html', context)

# - For drivers to edit their times
@login_required(login_url='login')
def driver_time_edit(request, id):
    user = get_object_or_404(NewUser, id=request.user.id)
    driver_time = get_object_or_404(DriverTimes, id=id, driver__user=user)
    user_productions = user.productions.filter(is_active=True)

    # Check if the user is a driver
    is_driver = Driver.objects.filter(user=user).exists()

    # Get the dot admin email from the production associated with the driver time
    production = get_object_or_404(Production, production_title=driver_time.production_title)
    dot_admin_email = production.dot_admin_email

    if request.method == 'POST':
        # Update the driver time with the form data
        driver_time.call_time = Decimal(request.POST.get('call_time')) if request.POST.get('call_time') else driver_time.call_time
        driver_time.non_deducted_breakfast_in = Decimal(request.POST.get('non_deducted_breakfast_in')) if request.POST.get('non_deducted_breakfast_in') else driver_time.non_deducted_breakfast_in
        driver_time.lunch_1_out = Decimal(request.POST.get('lunch_1_out')) if request.POST.get('lunch_1_out') else driver_time.lunch_1_out
        driver_time.lunch_1_in = Decimal(request.POST.get('lunch_1_in')) if request.POST.get('lunch_1_in') else driver_time.lunch_1_in
        driver_time.lunch_2_out = Decimal(request.POST.get('lunch_2_out')) if request.POST.get('lunch_2_out') else driver_time.lunch_2_out
        driver_time.lunch_2_in = Decimal(request.POST.get('lunch_2_in')) if request.POST.get('lunch_2_in') else driver_time.lunch_2_in
        driver_time.non_deducted_meal_out = Decimal(request.POST.get('non_deducted_meal_out')) if request.POST.get('non_deducted_meal_out') else driver_time.non_deducted_meal_out
        driver_time.non_deducted_meal_in = Decimal(request.POST.get('non_deducted_meal_in')) if request.POST.get('non_deducted_meal_in') else driver_time.non_deducted_meal_in
        driver_time.wrap_time = Decimal(request.POST.get('wrap_time')) if request.POST.get('wrap_time') else driver_time.wrap_time
        driver_time.total_hours = Decimal(request.POST.get('total_hours')) if request.POST.get('total_hours') else driver_time.total_hours
        driver_time.notes = request.POST.get('notes') or driver_time.notes
        driver_time.times_status = None

        # Save the updated driver time
        driver_time.save()

        # Add a new comment if provided
        comment_text = request.POST.get('comment')
        if comment_text:
            DriverTimeComment.objects.create(driver_time=driver_time, user=user, comment=comment_text)
        
        subject = f'Driver time edit by {driver_time.driver.first_name} {driver_time.driver.last_name} for {driver_time.work_date}'
        body = f"""
            
            {driver_time.driver.first_name} {driver_time.driver.last_name} has edited times for {driver_time.work_date}. Please review

            """
        print(f"Email Sent to {dot_admin_email}")
        recipient_list = [dot_admin_email]
        email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list)
        email.send(fail_silently=False)


        return redirect('driver_times_history')  # Redirect to the driver times history page after saving

    context = {
        'driver_time': driver_time,
        'user_productions': user_productions,
        'is_driver': is_driver,
        'comments': driver_time.comments.all(),
    }
    return render(request, 'interface/driver_time_edit.html', context)

# - Create a new run
@login_required(login_url='login')
def new_run(request):
    user = request.user

    initial_data = {
        'requester_name': f"{request.session.get('first_name')} {request.session.get('last_name')}",
        'requester_phone': request.session.get('phone_number'),
        'requester_email': request.session.get('user_email'),
        'requester_department': request.session.get('department'),
        'production_title': request.session.get('production_title'),
    }

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Check if the user is a driver
    is_driver = Driver.objects.filter(user=user).exists()

    if request.method == "POST":
        run = NewRunRequest(request.POST, request.FILES)
        if run.is_valid():
            instance = run.save(commit=False)
            instance.run_status = "Open"
            instance.save()

            # Fetch the requester's email from the session data
            requester_email = request.session.get('email')

            # Fetch the production title from the session data
            production_title = request.session.get('production_title')
            production = get_object_or_404(Production, production_title=production_title)

            # Fetch the captain's email based on the production title
            captain_email = production.captain_email

            # Construct the URL to the run
            run_url = f"https://www.ontheday.app/run/{instance.id}"

            # Send an email to the requester
            requester_email_message = EmailMessage(
                subject=f'Run Request #{instance.id} to {instance.pickup_name} Submitted',
                body=f'Thank you for submitting a run request, {instance.requester_name}. Your request is now open. You can view the details of your run here: {run_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[requester_email],
                reply_to=[captain_email],
            )
            requester_email_message.send(fail_silently=False)


            # Send an email to the captain
            captain_email_message = EmailMessage(
                subject=f'New Run Submitted by {instance.requester_department}',
                body=f'A new run has been submitted by {instance.requester_name}. You can view the details of the run here: {run_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[captain_email],
                reply_to=[requester_email],
            )
            captain_email_message.send(fail_silently=False)


            return redirect("dashboard")
        else:
            print(run.errors)  # Debugging line to print form errors

    else:
        run = NewRunRequest(initial=initial_data)

    context = {
        'run': run,
        'user_productions': user_productions,
        'is_driver': is_driver,
    }
    return render(request, 'interface/new_run.html', context)

# - Update a run
@login_required(login_url='login')
def update_run(request, run_request_id):
    run_request = get_object_or_404(RunRequest, id=run_request_id)

    if request.method == 'POST':
        form = NewRunRequest(request.POST, instance=run_request)
        if form.is_valid():
            form.save()
            print("Run updated successfully")  # Debugging line
            return redirect('run_queue')  # Redirect to the run queue or another appropriate page
        else:
            print("Form is not valid")  # Debugging line
            print(form.errors)  # Debugging line to print form errors
    else:
        form = NewRunRequest(instance=run_request)
        print("GET request - form initialized")  # Debugging line

    context = {
        'form': form,
        'run_request': run_request,
    }
    return render(request, 'interface/run.html', context)

# - Complete a run
@login_required(login_url='login')
def complete_run(request, run_request_id):
    run = get_object_or_404(RunRequest, id=run_request_id)
    run.run_status = "Completed"
    run.save()

    # Fetch the requester's email from the run instance
    requester_email = run.requester_email

    # Fetch the production title from the session data
    production_title = request.session.get('production_title')
    production = get_object_or_404(Production, production_title=production_title)

    # Fetch the captain's email based on the production title
    captain_email = production.captain_email

    # Construct the URL to the run
    run_url = f"https://www.ontheday.app/run/{run.id}"

    # Send an email to the requester
    complete_email_message = EmailMessage(
        subject=f'Run Request #{run.id} has been completed',
        body=f'Your run has been completed. You can view the details of your run here: {run_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[requester_email],
        reply_to=[captain_email],
    )
    complete_email_message.send(fail_silently=False)

    
    # Get the referer URL
    referer = request.META.get('HTTP_REFERER')
    
    # Redirect to the referer if it's present, otherwise fallback to a default page
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect('dashboard')

# - Cancel a run
@login_required(login_url='login')
def cancel_run(request, run_request_id):
    run = get_object_or_404(RunRequest, id=run_request_id)
    run.run_status = "Cancelled"
    run.save()

    # Fetch the requester's email from the run instance
    requester_email = run.requester_email

    # Fetch the production title from the session data
    production_title = request.session.get('production_title')
    production = get_object_or_404(Production, production_title=production_title)

    # Fetch the captain's email based on the production title
    captain_email = production.captain_email


    # Construct the URL to the run
    run_url = f"https://www.ontheday.app/run/{run.id}"

    # Send an email to the requester
    cancel_email_message = EmailMessage(
        subject=f'Run Request #{run.id} Cancelled',
        body=f'Your run has been cancelled. You can view the details of your run here: {run_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[requester_email],
        reply_to=[captain_email],
    )
    cancel_email_message.send(fail_silently=False)
    
    # Get the referer URL
    referer = request.META.get('HTTP_REFERER')
    
    # Redirect to the referer if it's present, otherwise fallback to a default page
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect('dashboard')

# Run History
@login_required(login_url='login')
def run_history(request):
    # Fetch RunRequest data model
    runs = RunRequest.objects.all()

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Check if the user is a driver
    driver = Driver.objects.filter(user=user).first()
    is_driver = driver is not None

    # Filter runs by production_title in session
    production_title_in_session = request.session.get('production_title')
    if production_title_in_session:
        runs = runs.filter(production_title=production_title_in_session)

    # Filter runs by user's department
    user_department = request.session.get('department')
    if user_department not in ['Admin', 'Production', 'Transportation']:
        runs = runs.filter(requester_department=user_department)

    # If the user is a driver, only show runs where the user is an assigned driver
    if is_driver:
        runs = runs.filter(assigned_driver=driver)

    # Pass the objects to the template context
    context = {
        'runs': runs,
        'user_productions': user_productions,
        'is_driver': is_driver,
    }
    return render(request, 'interface/run_history.html', context=context)

# Run Queue
@login_required(login_url='login')
def run_queue(request):
    # Fetch RunRequest data model
    runs = RunRequest.objects.exclude(run_status__in=["Completed", "Cancelled"]).order_by('run_date', 'need_by_this_time')

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Check if the user is a driver
    driver = Driver.objects.filter(user=user).first()
    is_driver = driver is not None

    # Filter runs by production_title in session
    production_title_in_session = request.session.get('production_title')
    if production_title_in_session:
        runs = runs.filter(production_title=production_title_in_session)

    # Filter runs by user's department
    user_department = request.session.get('department')
    if user_department not in ['Admin', 'Production', 'Transportation']:
        runs = runs.filter(requester_department=user_department)

    # If the user is a driver, only show runs where the user is an assigned driver
    if is_driver:
        runs = runs.filter(assigned_driver=driver)

    # Pass the objects to the template context
    context = {
        'runs': runs,
        'user_productions': user_productions,
        'is_driver': is_driver,
    }
    return render(request, 'interface/run_queue.html', context=context)

@login_required(login_url='login')
def acknowledge_run(request, run_id):
    run = get_object_or_404(RunRequest, id=run_id)
    run.run_status = 'In Progress'
    run.save()

    # Fetch the requester's email from the run instance
    requester_email = run.requester_email

    # Fetch the production title from the session data
    production_title = request.session.get('production_title')
    production = get_object_or_404(Production, production_title=production_title)

    # Fetch the captain's email based on the production title
    captain_email = production.captain_email

    # Send an email to the requester
    acknowledge_email_message = EmailMessage(
        subject=f'Run Request #{run.id} is in progress',
        body=f'Hello {run.requester_name},\n\nRun {run.id} to {run.pickup_name } is currently in progress.\n\nThank you.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[requester_email],
        reply_to=[captain_email],
    )

    acknowledge_email_message.send(fail_silently=False)

    return redirect('run_queue')

# View Run
@login_required(login_url='login')
def view_run(request, run_request_id):
    # Fetch the production title from the session data
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)
    
    run = get_object_or_404(RunRequest, id=run_request_id)

    # Check if the production title in the session matches the run's production title
    session_production_title = request.session.get('production_title')
    if session_production_title != run.production_title:
        return redirect('dashboard')  # Redirect to the dashboard if titles don't match

    error_message = None
    if request.method == 'POST':
        form = NewRunRequest(request.POST, instance=run)
        if form.is_valid():
            form.save()
            return redirect('view_run', run_request_id=run.id)
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
            error_message = "Please correct the errors below."
    else:
        form = NewRunRequest(instance=run)

    # Get active drivers with the same production title
    active_drivers = Driver.objects.filter(is_active=True, production_title=run.production_title)
    print("Active Drivers:", active_drivers)

    # Get truck sizes from the form
    truck_sizes = NewRunRequest.TRUCK_SIZE_CHOICES
    print("Truck Sizes:", truck_sizes)

    context = {
        'form': form,
        'run': run,
        'user_productions': user_productions,
        'active_drivers': active_drivers,
        'truck_sizes': truck_sizes,
    }
    return render(request, 'interface/run.html', context)

@login_required(login_url='login')
def equipment_admin(request):
    vehicles = Equipment.objects.all()
    picture_cars = PictureCars.objects.all()

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

     # Filter runs by production_title in session
    production_title_in_session = request.session.get('current_production_id')
    if production_title_in_session:
        vehicles = vehicles.filter(production_title=production_title_in_session)
        picture_cars = picture_cars.filter(production_title=production_title_in_session)

    context = {
        'vehicles': vehicles,
        'picture_cars': picture_cars,
        'user_productions': user_productions,
    }

    return render(request, 'interface/equipment_admin.html', context=context)

@login_required(login_url='login')
def add_truck(request):
        # Fetch the production title from the session data
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    if request.method == 'POST':
        form = NewEquipment(request.POST)
        if form.is_valid():
            try:
                # Retrieve production_title from the session
                production_title = request.session.get('production_title')
                if not production_title:
                    return render(request, 'interface/add_truck.html', {'form': form, 'error': 'Production title is missing from session.'})

                # Retrieve or create the Production instance
                production, created = Production.objects.get_or_create(production_title=production_title)

                # Save the Equipment instance with the production_title
                equipment = form.save(commit=False)
                equipment.production_title = production
                equipment.save()
                form.save_m2m()  # Save the many-to-many relationships

                return redirect('equipment_admin')  # Redirect to the equipment list page
            except Exception as e:
                print(f"Error saving equipment: {e}")
                return render(request, 'interface/add_truck.html', {'form': form, 'error': str(e)})
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = NewEquipment()

    context = {
        'form': form,
        'user_productions': user_productions,
    }

    return render(request, 'interface/add_truck.html', context=context)

@login_required(login_url='login')
def add_trailer(request):
        # Fetch the production title from the session data
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    if request.method == 'POST':
        form = NewEquipment(request.POST)
        if form.is_valid():
            try:
                # Retrieve production_title from the session
                production_title = request.session.get('production_title')
                if not production_title:
                    return render(request, 'interface/add_trailer.html', {'form': form, 'error': 'Production title is missing from session.'})

                # Retrieve or create the Production instance
                production, created = Production.objects.get_or_create(production_title=production_title)

                # Save the Equipment instance with the production_title
                equipment = form.save(commit=False)
                equipment.production_title = production
                equipment.save()
                form.save_m2m()  # Save the many-to-many relationships

                return redirect('equipment_admin')  # Redirect to the equipment list page
            except Exception as e:
                print(f"Error saving equipment: {e}")
                return render(request, 'interface/add_trailer.html', {'form': form, 'error': str(e)})
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = NewEquipment()

    context = {
        'form': form,
        'user_productions': user_productions,
    }

    return render(request, 'interface/add_trailer.html', context=context)

@login_required(login_url='login')
def add_picture_cars(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)
    production_title = request.session.get('production_title')
    if not production_title:
        return render(request, 'interface/add_picture_cars.html', {'error': 'Production title is missing from session.'})

    production = Production.objects.filter(production_title=production_title).first()
    if request.method == 'POST':
        form = NewPictureCars(request.POST, production_title_initial=production)
        if form.is_valid():
            try:
                # Save the PictureCars instance with the production_title
                picture_car = form.save(commit=False)
                picture_car.production_title = production
                picture_car.save()

                return redirect('picture_cars_list')  # Redirect to the picture cars list page
            except Exception as e:
                print(f"Error saving picture car: {e}")
                return render(request, 'interface/add_picture_cars.html', {'form': form, 'error': str(e)})
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = NewPictureCars(production_title_initial=production)

    context = {
        'form': form,
        'user_productions': user_productions,
    }

    return render(request, 'interface/add_picture_cars.html', context=context)

@login_required(login_url='login')
def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'interface/equipment_list.html', {'equipment': equipment})

@login_required(login_url='login')
def daily_rundown(request):

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    production_title = request.session.get('production_title')
    if not production_title:
        return render(request, 'interface/daily_rundown.html', {'error': 'Production title is missing from session.'})

    production = get_object_or_404(Production, production_title=production_title)
    date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
    date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date object
    day_of_week = date.strftime('%A')  # Get the day of the week

    # Fetch the rundown for the selected date, if it exists
    try:
        rundown = DriverDailyRundown.objects.get(production=production, date=date)
        drivers = rundown.drivers.all()
        equipment = rundown.equipment.all()
        driver_times = DriverTimes.objects.filter(driver__in=drivers, work_date=date, production_title=production_title)
    except DriverDailyRundown.DoesNotExist:
        rundown = None
        drivers = Driver.objects.none()
        equipment = Equipment.objects.none()
        driver_times = DriverTimes.objects.none()

    # Print the driver IDs to the console
    for driver in drivers:
        print("Driver ID:", driver.id)

    # Divide drivers by production status
    on_production_drivers = drivers.filter(production_status='On Production')
    off_production_drivers = drivers.filter(production_status='Off Production')
 
    # Debugging: Print the fetched driver_times
    for dt in driver_times:
        print("Driver Times:",driver_times)

    context = {
        'rundown': rundown,
        'production': production,
        'date': date_str,  # Pass the date string for display
        'day_of_week': day_of_week,  # Include the day of the week in the context
        'on_production_drivers': on_production_drivers,
        'off_production_drivers': off_production_drivers,
        'driver_times': driver_times,
        'equipment': equipment,
        'user_productions': user_productions,
        
    }
    return render(request, 'interface/daily_rundown.html', context)

@login_required(login_url='login')
def add_driver_to_rundown(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    production_title = request.session.get('production_title')
    if not production_title:
        return render(request, 'interface/add_driver_to_rundown.html', {'error': 'Production title is missing from session.'})

    production = get_object_or_404(Production, production_title=production_title)
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        driver = get_object_or_404(Driver, id=driver_id)

        rundown, created = DriverDailyRundown.objects.get_or_create(
            production=production,
            date=date,
        )
        rundown.drivers.add(driver)
        # Update driver information for the specific day
        driver.driver_phone = request.POST.get('driver_phone')
        driver.last_4 = request.POST.get('last_4')
        driver.assigned_vehicle = request.POST.get('assigned_vehicle')
        driver.driver_email = request.POST.get('driver_email')
        driver.save()
        return redirect(f"{reverse('daily_rundown')}?date={date_str}")

    drivers = Driver.objects.filter(production_title=production_title, is_active=True).exclude(driverdailyrundown__date=date)
    context = {
        'drivers': drivers,
        'date': date_str,
        'user_productions': user_productions,
    }
    return render(request, 'interface/add_driver_to_rundown.html', context)

@login_required(login_url='login')
def driver_info(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    # Fetch the latest rundown for the driver to get the instructions
    rundown = DriverDailyRundown.objects.filter(drivers=driver).order_by('-date').first()
    instructions = rundown.instructions if rundown else ''
    data = {
        'driver_phone': driver.driver_phone,
        'last_4': driver.last_4,
        'assigned_vehicle': driver.assigned_vehicle,
        'email': driver.driver_email,
        'notes': instructions,
    }
    return JsonResponse(data)

@login_required(login_url='login')
def remove_driver_from_rundown(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        date_str = request.POST.get('date')
        production_title = request.session.get('production_title')
        production = get_object_or_404(Production, production_title=production_title)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        rundown = get_object_or_404(DriverDailyRundown, production=production, date=date)
        driver = get_object_or_404(Driver, id=driver_id)
        rundown.drivers.remove(driver)

        return redirect(f"{reverse('daily_rundown')}?date={date_str}")

@login_required(login_url='login')
def save_rundown(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        production_title = request.session.get('production_title')
        production = get_object_or_404(Production, production_title=production_title)
        date_str = data.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        rundown, created = DriverDailyRundown.objects.get_or_create(
            production=production,
            date=date,
        )

        rundown.drivers.clear()
        rundown.equipment.clear()
        rundown.driver_times.clear()

        for driver_data in data.get('drivers', []):
            if 'id' in driver_data:
                driver = get_object_or_404(Driver, id=driver_data['id'])
            else:
                driver = Driver.objects.create(
                    first_name=driver_data['first_name'],
                    last_name=driver_data['last_name'],
                    driver_phone=driver_data['driver_phone'],
                    last_4=driver_data['last_4'],
                    is_active=True
                )
            rundown.drivers.add(driver)

        for equipment_data in data.get('equipment', []):
            equipment = get_object_or_404(Equipment, id=equipment_data['id'])
            rundown.equipment.add(equipment)

        for driver_time_data in data.get('driver_times', []):
            driver_time = get_object_or_404(DriverTimes, id=driver_time_data['id'])
            rundown.driver_times.add(driver_time)

        rundown.save()
        return JsonResponse({'status': 'success'})

@login_required(login_url='login')
def copy_rundown(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        production_title = request.session.get('production_title')
        production = get_object_or_404(Production, production_title=production_title)
        date_str = data.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        next_date = date + timedelta(days=1)

        rundown, created = DriverDailyRundown.objects.get_or_create(
            production=production,
            date=next_date,
        )

        if not created:
            rundown.drivers.clear()
            rundown.equipment.clear()
            rundown.driver_times.clear()

        original_rundown = get_object_or_404(DriverDailyRundown, production=production, date=date)
        for driver in original_rundown.drivers.all():
            rundown.drivers.add(driver)
        for equipment in original_rundown.equipment.all():
            rundown.equipment.add(equipment)
        for driver_time in original_rundown.driver_times.all():
            rundown.driver_times.add(driver_time)

        rundown.save()
        return JsonResponse({'status': 'success'})
# - Search Drivers on daily rundown
@login_required(login_url='login')
def search_active_drivers(request):
    query = request.GET.get('query', '')
    date_str = request.GET.get('date', '')
    production_title = request.session.get('production_title')
    production = get_object_or_404(Production, production_title=production_title)
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Get drivers already on the sheet for the selected date
    try:
        rundown = DriverDailyRundown.objects.get(production=production, date=date)
        existing_driver_ids = rundown.drivers.values_list('id', flat=True)
    except DriverDailyRundown.DoesNotExist:
        existing_driver_ids = []

    drivers = Driver.objects.filter(production_title=production_title, is_active=True).exclude(id__in=existing_driver_ids)

    results = []
    for driver in drivers:
        results.append({'id': driver.id, 'first_name': driver.first_name, 'last_name': driver.last_name})

    return JsonResponse({'drivers': results})

@login_required(login_url='login')
def search_drivers_and_equipment(request):
    query = request.GET.get('query', '')
    production_title = request.session.get('production_title')
    production = get_object_or_404(Production, production_title=production_title)

    drivers = Driver.objects.filter(production_title=production_title, is_active=True, first_name__icontains=query) | Driver.objects.filter(production_title=production_title, is_active=True, last_name__icontains=query)
    equipment = Equipment.objects.filter(production_title=production, is_active=True, vehicle_type__icontains=query) | Equipment.objects.filter(production_title=production, is_active=True, vendor_unit_number__icontains=query)

    results = []
    for driver in drivers:
        results.append({'id': driver.id, 'name': f"{driver.first_name} {driver.last_name}", 'type': 'driver'})
    for equip in equipment:
        results.append({'id': equip.id, 'name': f"{equip.vehicle_type} {equip.vendor_unit_number}", 'type': 'equipment'})

    return JsonResponse({'results': results})

@login_required(login_url='login')
def radios(request):
    return render(request, 'interface/radios.html')

@login_required(login_url='login')
def radio_scan(request):
    if request.method == 'POST':
        form = RadioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('radios')
    else:
        form = RadioForm()
    return render(request, 'interface/radios.html', {'form': form})

# Change Production
@login_required(login_url='login')
def change_production(request):
    if request.method == 'POST':
        production_title = request.POST.get('production_title')

        # Query the Production object based on the selected production_title
        production = get_object_or_404(Production, production_title=production_title)

        # Set session variables
        request.session['current_production_id'] = production.id
        request.session['production_title'] = production.production_title

        # Redirect to the 'next' URL if it exists, otherwise redirect to 'dashboard'
        next_url = request.POST.get('next', 'dashboard')
        return redirect(next_url)

    # If GET request or form submission failed, handle accordingly (optional)

    # Retrieve all productions
    user_productions = Production.objects.all()

    # Check if there is an active production in session
    current_production_id = request.session.get('current_production_id')
    if current_production_id:
        production = get_object_or_404(Production, id=current_production_id)
    else:
        # If no active production in session, select the first production in the list
        production = user_productions.first()  # You might want to order this query if needed

        # Set session variables for the default production
        request.session['current_production_id'] = production.id
        request.session['production_title'] = production.production_title

    return render(request, 'interface/dashboard.html', {'user_productions': user_productions, 'selected_production': production})

# Search Locations
def search_locations(request):
    query = request.GET.get('query', '')
    search_type = request.GET.get('type', 'pickup')  # 'pickup' or 'dropoff'
    production_title_in_session = request.session.get('production_title', '')

    if query:
        vendor_results = Vendor.objects.filter(vendor_name__icontains=query)[:5]
        location_results = Location.objects.filter(
            location_name__icontains=query,
            production_title=production_title_in_session
        )[:5]

        data = []
        
        for vendor in vendor_results:
            data.append({
                'type': 'vendor',
                'name': vendor.vendor_name,
                'address_1': vendor.vendor_address_1,
                'address_2': vendor.vendor_address_2,
                'city': vendor.vendor_city,
                'state': vendor.vendor_state,
                'zip': vendor.vendor_zip,
                'search_type': search_type
            })
        
        for location in location_results:
            data.append({
                'type': 'location',
                'name': location.location_name,
                'address_1': location.location_address_1,
                'address_2': location.location_address_2,
                'city': location.location_city,
                'state': location.location_state,
                'zip': location.location_zip,
                'search_type': search_type
            })
        
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)

# Search Users 
def search_user_by_email(request):
    email = request.GET.get('email', '')
    users = NewUser.objects.filter(email__icontains=email)
    user_list = [{'email': user.email} for user in users]
    response = {'exists': bool(user_list), 'users': user_list}
    return JsonResponse(response)

# Get User Details by Email
def get_user_details_by_email(request):
    # Get the email from the request
    email = request.GET.get('email', None)
    # Get the production_title from the session
    production_title = request.session.get('production_title', '')

    if email:
        try:
            user = NewUser.objects.get(email=email)
            # Assign the production_title from the session to the user's productions
            if production_title:
                production, created = Production.objects.get_or_create(production_title=production_title)
                user.productions.add(production)
            response = {
                'exists': True,
                'user': {
                    'production_title': production_title,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_name': user.username,
                    'driver_email': user.email,
                    'driver_phone': user.phone_number,
                }
            }
        except NewUser.DoesNotExist:
            response = {'exists': False}
    else:
        response = {'exists': False}
    
    return JsonResponse(response)

# fuel log
@login_required(login_url='login')
def fuel_log(request):
   return render(request, 'interface/fuel_log.html')

@login_required(login_url='login')
def purchase_order(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)
    purchase_orders = PurchaseOrders.objects.all()

    context = {
        'user_productions': user_productions,
        'purchase_orders': purchase_orders,
    }
    return render(request, 'interface/purchase_order.html', context=context)

@login_required(login_url='login')
def add_purchase_order(request):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    if request.method == 'POST':
        form = PurchaseOrdersForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST, instance=form.instance)
        if form.is_valid() and formset.is_valid():
            purchase_order = form.save()
            formset.instance = purchase_order
            formset.save()
            return redirect('purchase_order')  # Redirect to the list of purchase orders after saving
    else:
        form = PurchaseOrdersForm()
        formset = PurchaseOrderItemFormSet(instance=PurchaseOrders())

    context = {
        'user_productions': user_productions,
        'form': form,
        'formset': formset,
    }
    return render(request, 'interface/add_purchase_order.html', context=context)

@login_required(login_url='login')
def view_purchase_order(request, purchase_order_id):
    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)
    purchase_order = get_object_or_404(PurchaseOrders, id=purchase_order_id)

    context = {
        'user_productions': user_productions,
        'purchase_order': purchase_order,
    }
    return render(request, 'interface/view_purchase_order.html', context=context)