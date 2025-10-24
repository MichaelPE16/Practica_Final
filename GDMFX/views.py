from django.shortcuts import render

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
    return render(request, 'login.html')

def signup_page(request): 
    return render(request, 'signup.html')

def meets(request): 
    return render(request, 'meets.html')

def reports(request): 
    return render(request, 'reports.html')

def sales(request): 
    return render(request, 'sales.html')

def show_details(request): 
    return render(request, 'show_details.html')

def show_forms(request): 
    return render(request, 'show_forms.html')