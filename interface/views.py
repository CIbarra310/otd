from .forms import LoginForm, CreateUserForm
from core.models import Production, Vendor, Location
from collections import defaultdict
from transportation.forms import NewRunRequest, RunRequest, NewDriver, Driver
from production.forms import RadioForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.models import Production, NewUser
import json

# - Home Page
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # You can use the name of the URL pattern for the dashboard page
    else:
        return render(request, 'interface/index.html')


# - Register a new user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        
    context = {'form':form}  
    return render(request, 'interface/register.html', context = context) 

# - Login an existing user
def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
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
                request.session['user_name'] = user.user_name
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

# - Dashboard Page
@login_required(login_url=login)
def dashboard(request):
    # Fetch RunRequest data model filtered by production_title in session
    runs = RunRequest.objects.all().order_by('-run_date')

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Filter runs by production_title in session
    production_title_in_session = request.session.get('production_title')
    if production_title_in_session:
        runs = runs.filter(production_title=production_title_in_session)

    # Pass the objects to the template context
    context = {
        'runs': runs,
        'user_productions': user_productions,
    }
    return render(request, 'interface/dashboard.html', context=context)

# - Driver roster page
@login_required(login_url='login')
def driver_roster(request):
    drivers = Driver.objects.all()

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    context = {
        'drivers': drivers,
        'user_productions': user_productions,
    }
    return render(request, 'interface/driver_roster.html', context=context)

@login_required(login_url=login)
def add_driver(request):
    if request.method == "POST":
        driver = NewDriver(request.POST)
        if driver.is_valid():
            driver.save()
            return redirect("driver_roster")
        else:
           messages.error(request, "There was an error with your submission. Please check the form for errors.")

    driver = NewDriver()
    context = {'driver': driver}
    return render(request, 'interface/add_driver.html', context=context)

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
    return render(request, 'interface/driver.html', {'driver': driver})

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

    if request.method == "POST":
        run = NewRunRequest(request.POST, request.FILES)
        if run.is_valid():
            instance = run.save(commit=False)
            instance.run_status = "Open"
            instance.save()

            # Send confirmation emails
            subject = 'Run Request #{instance.id} to {instance.pickup_name} Submitted'
            message = f'Thank you for submitting a run request, {instance.requester_name}. Your request is now open.'
            from_email = 'admin@ontheday.app'
            recipient_list = [instance.requester_email]

            #send_mail(
            #   subject,
            #    message,
            #    from_email,
            #    recipient_list,
            #    fail_silently=False,
            #)
            
            return redirect("dashboard")
        else:
            print(run.errors)  # Debugging line to print form errors

    else:
        run = NewRunRequest(initial=initial_data)

    context = {
        'run': run,
        'user_productions': user_productions,
    }
    return render(request, 'interface/new_run.html', context)

@login_required(login_url='login')
def complete_run(request, run_request_id):
    run = get_object_or_404(RunRequest, id=run_request_id)
    run.run_status = "Completed"
    run.save()
    
    # Get the referer URL
    referer = request.META.get('HTTP_REFERER')
    
    # Redirect to the referer if it's present, otherwise fallback to a default page
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def cancel_run(request, run_request_id):
    run = get_object_or_404(RunRequest, id=run_request_id)
    run.run_status = "Cancelled"
    run.save()
    
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

    # Filter runs by production_title in session
    production_title_in_session = request.session.get('production_title')
    if production_title_in_session:
        runs = runs.filter(production_title=production_title_in_session)

    # Pass the objects to the template context
    context = {
        'runs': runs,
        'user_productions': user_productions,
    }
    return render(request, 'interface/run_history.html', context=context)

# Run History
@login_required(login_url='login')
def run_queue(request):
    # Fetch RunRequest data model
    runs = RunRequest.objects.exclude(run_status__in=["Completed","Cancelled"]).order_by('run_date', 'need_by_this_time')

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    # Filter runs by production_title in session
    production_title_in_session = request.session.get('production_title')
    if production_title_in_session:
        runs = runs.filter(production_title=production_title_in_session)

    # Pass the objects to the template context
    context = {
        'runs': runs,
        'user_productions': user_productions,
    }
    return render(request, 'interface/run_queue.html', context=context)

@login_required(login_url='login')
def view_run(request, run_request_id):
    run_request = get_object_or_404(RunRequest, id=run_request_id)

    # Fetch current user's productions
    user = get_object_or_404(NewUser, id=request.user.id)
    user_productions = user.productions.filter(is_active=True)

    context = {
        'run_request': run_request,
        'user_productions': user_productions,
    }

    return render(request, 'interface/run.html', context=context)

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

@login_required(login_url='login')
def change_production(request):
    if request.method == 'POST':
        production_title = request.POST.get('production_title')

        # Query the Production object based on the selected production_title
        production = get_object_or_404(Production, production_title=production_title)

        # Set session variables
        request.session['current_production_id'] = production.id
        request.session['production_title'] = production.production_title

        return redirect('dashboard')

    # If GET request or form submission failed, handle accordingly (optional)

    return redirect('dashboard')

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