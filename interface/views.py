from .forms import LoginForm, CreateUserForm
from transportation.forms import RunRequest, NewRunRequest
from production.forms import RadioForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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

# - Create a new run
def new_run(request):
    # Get logged-in user's data
    user = request.user
    requester_name = f"{user.first_name} {user.last_name}"
    requester_phone = user.phone_number
    requester_email = user.email
    requester_department = user.department

    # Create a dictionary with the user data
    initial_data = {
        'requester_name': requester_name,
        'requester_phone': requester_phone,
        'requester_email': requester_email,
        'requester_department': requester_department,
    }

    if request.method == "POST":
        # If it's a POST request, process the form data
        run = NewRunRequest(request.POST)
        if run.is_valid():
            # Process the form data
            run.save()
            return redirect("dashboard")
    else:
        # If it's not a POST request, create a new form instance with initial data
        run = NewRunRequest(initial=initial_data)

    context = {'run': run}
    return render(request, 'interface/new_run.html', context=context)

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
