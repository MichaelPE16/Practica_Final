from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError


# Create your views here.
def home(request): 
    return render(request, 'home.html')

def contract(request): 
    return render(request, 'contract.html')

def dashboard(request): 
    return render(request, 'dashboard.html')

def inventory(request): 
    return render(request, 'inventory.html')

def leads(request): 
    return render(request, 'leads.html')

def login_page(request):
    if request.method == "GET":
        return render(request, 'login.html', {'form': AuthenticationForm})
    else: 
        log_username = request.POST['username']
        log_password = request.POST['password']
        user = authenticate(request, username = log_username, password = log_password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'form': AuthenticationForm, 'error': 'User Or Password Incorrect'})




def signup_page(request):
    if request.method == 'GET': 
        return render(request, 'signup.html', {'form': UserCreationForm})
    else: 
        if request.POST['password1'] == request.POST['password2']: 
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('login')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'User already exist'})
            
    return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Passwords do not match'})

def meets(request): 
    return render(request, 'meets.html')

def reports(request): 
    return render(request, 'reports.html')

def sales(request): 
    return render(request, 'sales.html')

def show_details(request, id_details): 
    return render(request, 'show_details.html')

def show_forms(request, id_forms): 
    return render(request, 'show_forms.html')