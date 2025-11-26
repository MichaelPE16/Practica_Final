from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
#here the modules to start pagination
from django.core.paginator import Paginator
from .forms import ContractForm, LeadsForm, SalesForm, VehicleForm
from .models import Contract, Leads, Sales, Vehicles



# Create your views here.
def home(request): 
    return render(request, 'home.html')

def contract(request): 
    contract = Contract.objects.filter(user=request.user)
    return render(request, 'contract.html',{'contracts': contract} )

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def inventory(request): 
    vehicle = Vehicles.objects.filter(user=request.user)
    return render(request, 'inventory.html',{'vehicles': vehicle} )

@login_required
def leads(request):
    leads = Leads.objects.filter(user=request.user)
    return render(request, 'leads.html',{'leads': leads} )


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

@login_required
def meets(request): 
    return render(request, 'meets.html')

@login_required
def reports(request): 
    return render(request, 'reports.html')

@login_required
def sales(request): 
    sale = Sales.objects.filter(user=request.user)
    return render(request, 'sales.html',{'sales': sale} )

@login_required
def show_details(request, id_details): 

    vehicle = get_object_or_404(Vehicles, pk= id_details, user = request.user)
    return render(request, 'show_details.html', {'vehicle': vehicle})

@login_required
def show_sales(request, id_sales): 

    sale = get_object_or_404(Sales, pk= id_sales, user = request.user)
    return render(request, 'show_sales.html', {'sales': sale})

@login_required
def show_lead(request, id_lead): 

    lead = get_object_or_404(Leads, pk= id_lead, user = request.user)
    return render(request, 'show_lead.html', {'leads': lead})

@login_required
def show_contract(request, id_contract): 

    contract = get_object_or_404(Contract, pk= id_contract, user = request.user)
    pdf_exists = False
    if contract.file_pdf and contract.file_pdf.name:
        try:
            pdf_exists = contract.file_pdf.storage.exists(contract.file_pdf.name)
        except Exception:
            pdf_exists = False
    return render(request, 'show_contract.html', {'contract': contract, 'pdf_exists': pdf_exists})

@login_required
def upload_contract_pdf(request, id_contract):
    contract = get_object_or_404(Contract, pk=id_contract, user=request.user)
    if request.method != 'POST' or 'pdf_file' not in request.FILES:
        return redirect('show_contract', id_contract=id_contract)
    pdf = request.FILES['pdf_file']
    content_type = getattr(pdf, 'content_type', '')
    name_lower = pdf.name.lower()
    if content_type != 'application/pdf' and not name_lower.endswith('.pdf'):
        return redirect('show_contract', id_contract=id_contract)
    filename = f"contract_{contract.id}.pdf"
    contract.file_pdf.save(filename, pdf, save=True)
    return redirect('show_contract', id_contract=id_contract)

@login_required
def show_forms(request, id_forms):
    return render(request, 'show_forms.html')

def signout(request): 
    logout(request)
    return redirect('login')
