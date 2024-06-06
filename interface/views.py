from .forms import LoginForm, CreateUserForm
from collections import defaultdict
from transportation.forms import NewRunRequest, RunRequest, NewDriver, Driver
from production.forms import RadioForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Production, NewUser
import json

# - Home Page
def home(request):
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
                return redirect("login")
    
    context = {'form':form}
    return render(request, 'interface/login.html', context=context)

# - Logout a user
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect("login")

# - Production Admin
@login_required(login_url=login)
def production_admin(request):
    productions = Production.objects.all()

    context = {'productions': productions}

    return render(request, 'interface/production_admin.html', context = context)

# - User Admin
@login_required(login_url=login)
def user_admin(request):
    users = NewUser.objects.all()

    context = {'users': users}

    return render(request, 'interface/user_admin.html', context = context)

# - Dashboard Page
@login_required(login_url=login)
def dashboard(request):
    # Fetch RunRequest data model
    # runs = RunRequest.objects.all()

    # Pass the object to the template context
    # context = {
    #    'runs': runs
    #}
    return render(request, 'interface/dashboard.html') #context=context

# - Driver roster page
@login_required(login_url='login')
def driver_roster(request):
    drivers = Driver.objects.all()

    context = {'drivers': drivers}
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


@login_required(login_url='login')
def activate_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    driver.is_active = True
    driver.save()
    return redirect('driver_roster')

@login_required(login_url='login')
def deactivate_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    driver.is_active = False
    driver.save()
    return redirect('driver_roster')

@login_required(login_url='login')
def driver_rundown(request):

    return render(request, 'interface/driver_rundown.html')

# - Create a new run
@login_required(login_url='login')
def new_run(request):
    user = request.user
    initial_data = {
        'requester_name': f"{user.first_name} {user.last_name}",
        'requester_phone': user.phone_number,
        'requester_email': user.email,
        'requester_department': user.department,
        'production_title': user.production_title,
    }

    if request.method == "POST":
        run = NewRunRequest(request.POST, request.FILES)
        if run.is_valid():
            instance = run.save(commit=False)
            instance.run_status = "Open"
            instance.save()
            return redirect("dashboard")
        else:
            print(run.errors)  # Debugging line to print form errors

    else:
        run = NewRunRequest(initial=initial_data)

    context = {'run': run}
    return render(request, 'interface/new_run.html', context)

@login_required(login_url='login')
def complete_run(request, run_request_id):
    run = get_object_or_404(RunRequest, id=run_request_id)
    run.run_status = "Completed"
    run.save()
    return redirect('run_history')

@login_required(login_url='login')
def cancel_run(request, run_request_id):
    run = get_object_or_404(RunRequest, id=run_request_id)
    run.run_status = "Cancelled"
    run.save()
    return redirect('run_history')

# Run History
@login_required(login_url='login')
def run_history(request):
    # Fetch RunRequest data model
    runs = RunRequest.objects.all()

    # Pass the object to the template context
    context = {
        'runs': runs
    }
    return render(request, 'interface/run_history.html', context=context)

# Run History
@login_required(login_url='login')
def run_queue(request):
    # Fetch RunRequest data model
    runs = RunRequest.objects.exclude(run_status__in=["Completed","Cancelled"]).order_by('run_date', 'need_by_this_time')

    # Pass the object to the template context
    context = {
        'runs': runs
    }
    return render(request, 'interface/run_queue.html', context=context)

@login_required(login_url='login')
def view_run(request, run_request_id):
    run_request = get_object_or_404(RunRequest, id=run_request_id)
    return render(request, 'interface/run.html', {'run_request': run_request})

@login_required(login_url='login')
def radios(request):
    return render(request, 'interface/radios.html')

def radio_scan(request):
    if request.method == 'POST':
        form = RadioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('radios')
    else:
        form = RadioForm()
    return render(request, 'interface/radios.html', {'form': form})
