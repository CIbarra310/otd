from .forms import LoginForm, CreateUserForm
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
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    
    context = {'form':form}
    return render(request, 'interface/login.html', context=context)

# - Logout a user
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect("login")