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

ITEMS_PER_PAGE = 10

# Create your views here.
def home(request): 
    return render(request, 'home.html')

@login_required
def contract(request): 
    contract = Contract.objects.filter(user=request.user)
    # Pagination
    paginator = Paginator(contract, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'contract.html',{'contracts': page_obj} )

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def inventory(request): 
    vehicle = Vehicles.objects.filter(user=request.user)
    # Pagination
    paginator = Paginator(vehicle, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory.html',{'vehicles': page_obj} )

@login_required
def leads(request):
    leads = Leads.objects.filter(user=request.user)
    # Pagination
    paginator = Paginator(leads, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'leads.html',{'leads': page_obj} )   


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
    # Pagination
    paginator = Paginator(sale, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sales.html',{'sales': page_obj} )

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

@login_required
def new_vehicle(request):
    if request.method == 'GET':
        form = VehicleForm()
        form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'inventory_form.html', {'form': form})
    form = VehicleForm(request.POST)
    form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
    if form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.user = request.user
        vehicle.save()
        return redirect('inventory')
    return render(request, 'inventory_form.html', {'form': form})

@login_required
def new_lead(request):
    if request.method == 'GET':
        form = LeadsForm()
        form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'lead_form.html', {'form': form})
    form = LeadsForm(request.POST)
    form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
    if form.is_valid():
        lead = form.save(commit=False)
        lead.user = request.user
        lead.save()
        return redirect('leads')
    return render(request, 'lead_form.html', {'form': form})

@login_required
def new_sale(request):
    if request.method == 'GET':
        form = SalesForm()
        return render(request, 'sales_form.html', {'form': form})
    form = SalesForm(request.POST)
    if form.is_valid():
        sale = form.save(commit=False)
        sale.user = request.user
        sale.save()
        return redirect('sales')
    return render(request, 'sales_form.html', {'form': form})

@login_required
def new_contract(request):
    if request.method == 'GET':
        form = ContractForm()
        form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'contract_form.html', {'form': form})
    form = ContractForm(request.POST, request.FILES)
    form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
    if form.is_valid():
        contract = form.save(commit=False)
        contract.user = request.user
        contract.save()
        return redirect('contract')
    return render(request, 'contract_form.html', {'form': form})
    


""" Here the update for the diferent modules"""
@login_required
def update_vehicle(request, id_vehicle):
    vehicle = get_object_or_404(Vehicles, pk=id_vehicle, user=request.user)
    if request.method == 'GET':
        form = VehicleForm(instance=vehicle)
        return render(request, 'update_inventory.html', {'form': form, 'vehicle': vehicle})
    form = VehicleForm(request.POST, instance=vehicle)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('inventory')
    return render(request, 'update_inventory.html', {'form': form, 'vehicle': vehicle})

@login_required
def update_lead(request, id_lead):
    lead = get_object_or_404(Leads, pk=id_lead, user=request.user)
    if request.method == 'GET':
        form = LeadsForm(instance=lead)
        return render(request, 'update_lead.html', {'form': form, 'leads': lead})
    form = LeadsForm(request.POST, instance=lead)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('leads')
    return render(request, 'update_lead.html', {'form': form, 'leads': lead})

@login_required
def update_sale(request, id_sale):
    sale = get_object_or_404(Sales, pk=id_sale, user=request.user)
    if request.method == 'GET':
        form = SalesForm(instance=sale)
        return render(request, 'update_sell.html', {'form': form, 'sales': sale})

    form = SalesForm(request.POST, instance=sale)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user

        if obj.vehicle_sold:
            car = get_object_or_404(Vehicles, pk=obj.vehicle_sold.id, user=request.user)
            if obj.phase == "Closed":
                car.status = "Sold"
                car.save()

        obj.save()
        return redirect('sales')

    return render(request, 'update_sell.html', {'form': form, 'sales': sale})

@login_required
def update_contract(request, id_contract):
    contract = get_object_or_404(Contract, pk=id_contract, user=request.user)
    if request.method == 'GET':
        form = ContractForm(instance=contract)
        return render(request, 'update_contract.html', {'form': form, 'contract': contract})
    form = ContractForm(request.POST, request.FILES, instance=contract)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('contract')
    return render(request, 'update_contract.html', {'form': form, 'contract': contract})


# Here we create the update for the existing data in the sales, inventory, contracts and leads

"""Cambiar esta funtion"""
# @login_required
# def update_lead(request, id_lead):
#     lead = get_object_or_404(Leads, pk=id_lead, user=request.user)
#     if request.method == 'POST':
#         form = LeadsForm(request.POST, instance=lead)

#         if form.is_valid():
#             updated_lead = form.save(commit=False)
#             updated_lead.user = request.user
#             updated_lead.save()
#             return redirect('leads')
#     else:
#         form = LeadsForm(instance=lead)
#         form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
#         form.fields['user'].initial = request.user
#     return render(request, 'lead_form.html', {'form': form})
