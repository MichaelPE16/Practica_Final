from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, Count
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
#here the modules to start pagination
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import ContractForm, LeadsForm, SalesForm, VehicleForm, Apptform
from .models import Contract, Leads, Sales, Vehicles, Meets

ITEMS_PER_PAGE = 10

# Create your views here.
def home(request): 
    return render(request, 'home.html')

@login_required
def contract(request): 
    if request.method == "POST": 
        search =request.POST['search']
        idcontact = request.POST['ID']
        contract = Contract.objects.filter(user=request.user, customer_name__contains = search, id_document__contains =idcontact )
        paginator = Paginator(contract, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'contract.html',{'contracts': page_obj} )
    else: 
        contract = Contract.objects.filter(user=request.user)
    # Pagination
    paginator = Paginator(contract, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'contract.html',{'contracts': page_obj} )

@login_required
def dashboard(request):
    # Get filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    brand_filter = request.GET.get('brand')

    # Base QuerySets
    sales_qs = Sales.objects.filter(user=request.user)
    vehicles_qs = Vehicles.objects.filter(user=request.user)
    leads_qs = Leads.objects.filter(user=request.user)
    contracts_qs = Contract.objects.filter(user=request.user)

    # Apply date filters if provided
    if start_date:
        sales_qs = sales_qs.filter(selling_date__gte=start_date)
        contracts_qs = contracts_qs.filter(sign_date__gte=start_date)
        leads_qs = leads_qs.filter(contact_date__gte=start_date)
    if end_date:
        sales_qs = sales_qs.filter(selling_date__lte=end_date)
        contracts_qs = contracts_qs.filter(sign_date__lte=end_date)
        leads_qs = leads_qs.filter(contact_date__lte=end_date)
    
    if brand_filter and brand_filter != 'All Brands':
        vehicles_qs = vehicles_qs.filter(brand=brand_filter)
        contracts_qs = contracts_qs.filter(vehicle_sold__brand=brand_filter)
        sales_qs = sales_qs.filter(vehicle_sold__brand=brand_filter)

    # KPIs
    total_sales = sales_qs.filter(phase='Closed').count()
    total_revenue = contracts_qs.aggregate(total=Sum('price_sold'))['total'] or 0
    total_leads = leads_qs.count()
    inventory_value = vehicles_qs.filter(status='Available').aggregate(total=Sum('price_adquisition'))['total'] or 0

    # Common layout for dark theme
    dark_layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', family="Inter, sans-serif"),
        margin=dict(l=40, r=20, t=40, b=40)
    )

    # 1. Sales Trend (Line Chart) over Months
    sales_trend_html = ""
    contracts_list = list(contracts_qs.values('sign_date', 'price_sold'))
    if contracts_list:
        df_contracts = pd.DataFrame(contracts_list)
        df_contracts['sign_date'] = pd.to_datetime(df_contracts['sign_date'])
        df_contracts = df_contracts.dropna(subset=['sign_date'])
        if not df_contracts.empty:
            df_trend = df_contracts.groupby(df_contracts['sign_date'].dt.to_period('M')).agg({'price_sold':'sum'}).reset_index()
            df_trend['sign_date'] = df_trend['sign_date'].dt.to_timestamp()
            fig = px.line(df_trend, x='sign_date', y='price_sold', title='Revenue Trend ($)', markers=True)
            fig.update_layout(**dark_layout)
            fig.update_traces(line_color='#0d6efd')
            sales_trend_html = plot(fig, output_type='div', include_plotlyjs=False)

    # 2. Lead Status Distribution (Pie Chart)
    lead_status_html = ""
    leads_list = list(leads_qs.values('status'))
    if leads_list:
        df_leads = pd.DataFrame(leads_list)
        df_lead_status = df_leads['status'].value_counts().reset_index()
        df_lead_status.columns = ['status', 'count']
        fig = px.pie(df_lead_status, names='status', values='count', hole=0.4, title='Leads by Status',
                     color_discrete_sequence=px.colors.sequential.Teal)
        fig.update_layout(**dark_layout)
        lead_status_html = plot(fig, output_type='div', include_plotlyjs=False)

    # 3. Dispersions: Price vs KM (Scatter)
    scatter_html = ""
    vehicles_list = list(vehicles_qs.filter(condition='Used').values('km', 'selling_price', 'brand', 'model'))
    if vehicles_list:
        df_veh = pd.DataFrame(vehicles_list)
        df_veh['selling_price'] = df_veh['selling_price'].astype(float)
        df_veh = df_veh.dropna(subset=['km', 'selling_price'])
        if not df_veh.empty:
            df_veh['vehicle_name'] = df_veh['brand'] + " " + df_veh['model']
            fig = px.scatter(df_veh, x='km', y='selling_price', color='brand', hover_name='vehicle_name', title='Price vs Mileage (Used)')
            fig.update_layout(**dark_layout)
            scatter_html = plot(fig, output_type='div', include_plotlyjs=False)

    # 4. Inventory by Brand
    inventory_html = ""
    avail_veh_list = list(vehicles_qs.filter(status='Available').values('brand'))
    if avail_veh_list:
        df_inv = pd.DataFrame(avail_veh_list)
        df_inv_counts = df_inv['brand'].value_counts().reset_index()
        df_inv_counts.columns = ['brand', 'count']
        fig = px.bar(df_inv_counts, x='brand', y='count', title='Available Inventory by Brand', color='brand',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(**dark_layout)
        inventory_html = plot(fig, output_type='div', include_plotlyjs=False)
        
    all_brands = Vehicles.objects.filter(user=request.user).values_list('brand', flat=True).distinct()

    context = {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'total_leads': total_leads,
        'inventory_value': inventory_value,
        'sales_trend_html': sales_trend_html,
        'lead_status_html': lead_status_html,
        'scatter_html': scatter_html,
        'inventory_html': inventory_html,
        'all_brands': sorted(list(all_brands)),
        'start_date': start_date or '',
        'end_date': end_date or '',
        'brand_filter': brand_filter or '',
        'active_brands_list': [brand_filter] if brand_filter else ['All Brands'],
    }
    return render(request, 'dashboard.html', context)

@login_required
def inventory(request): 
    if request.method == 'POST': 
        search = request.POST['search']
        status = request.POST['status']
        vehicle = Vehicles.objects.filter(user=request.user, brand__contains = search, status = status)
        if status == 'All Statuses':
            vehicle = Vehicles.objects.filter(user=request.user, brand__contains = search)
        if search == '':
            vehicle = Vehicles.objects.filter(user=request.user, status = status)
        if search == '' and status == 'All Statuses':
            vehicle = Vehicles.objects.filter(user=request.user)
        paginator = Paginator(vehicle, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventory.html',
        {'vehicles': page_obj} )
    else: 
        vehicle = Vehicles.objects.filter(user=request.user)
    # Pagination
    paginator = Paginator(vehicle, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory.html',
    {'vehicles': page_obj} )

@login_required
def leads(request):
    if request.method == 'POST':
        search = request.POST['search']
        status = request.POST['status']
        leads = Leads.objects.filter(user=request.user, name__contains=search, status=status)
        if status == 'All Statuses':
            leads = Leads.objects.filter(user=request.user, name__contains=search)
        if search == '':
            leads = Leads.objects.filter(user=request.user, status=status)
        if search == '' and status == 'All Statuses':
            leads = Leads.objects.filter(user=request.user)
        
        paginator = Paginator(leads, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'leads.html', {'leads': page_obj})
    else:
        leads = Leads.objects.filter(user=request.user)
        # Pagination
        paginator = Paginator(leads, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'leads.html', {'leads': page_obj})


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
    search = request.POST.get('search', '')
    if request.method == 'POST' and search:
        meetings = Meets.objects.filter(
            Q(name__icontains=search) | Q(email__icontains=search),
            user=request.user
        ).order_by('-date')
    else:
        meetings = Meets.objects.filter(user=request.user).order_by('-date')
    
    paginator = Paginator(meetings, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'meets.html', {'meetings': page_obj})


def appt(request):
    if request.method == 'POST':
        form = Apptform(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'appt.html', {'success': True})
            except IntegrityError:
                form.add_error('date', 'This time slot is already taken. Please choose another.')
    else:
        form = Apptform()
    return render(request, 'appt.html', {'form': form})

@login_required
def reports(request): 
    return render(request, 'reports.html')

@login_required
def sales(request): 
    if request.method == "POST": 
        search = request.POST['search']
        if search:
            sale = Sales.objects.filter(
                Q(lead__name__contains=search) | Q(vehicle_sold__vin__contains=search),
                user=request.user
            )
        else:
            sale = Sales.objects.filter(user=request.user)
        paginator = Paginator(sale, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sales.html',{'sales': page_obj} )
    else: 
        sale = Sales.objects.filter(user=request.user)
        # Pagination
        paginator = Paginator(sale, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sales.html',{'sales': page_obj} )

#Este muestra los detalles de un vehiculo
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
        form.fields['user'].queryset = User.objects.filter(pk= request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'sales_form.html', {'form': form})
    form = SalesForm(request.POST)
    form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
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
        form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'contract_form.html', {'form': form})
    form = ContractForm(request.POST, request.FILES)
    form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
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
        form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'update_inventory.html', {'form': form})
    form = VehicleForm(request.POST, instance=vehicle)
    form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('inventory')
    return render(request, 'update_inventory.html', {'form': form})

@login_required
def update_lead(request, id_lead):
    lead = get_object_or_404(Leads, pk=id_lead, user=request.user)
    if request.method == 'GET':
        form = LeadsForm(instance=lead)
        form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'update_lead.html', {'form': form})
    form = LeadsForm(request.POST, instance=lead)
    form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('leads')
    return render(request, 'update_lead.html', {'form': form})
    

@login_required
def update_sale(request, id_sale):
    sale = get_object_or_404(Sales, pk=id_sale, user=request.user)
    if request.method == 'GET':
        form = SalesForm(instance=sale)
        form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'update_sell.html', {'form': form})

    form = SalesForm(request.POST, instance=sale)
    form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user

        if obj.phase == "Closed":
            # Update Lead status to Qualified
            obj.lead.status = "Qualified"
            obj.lead.save()

            if obj.vehicle_sold:
                car = get_object_or_404(Vehicles, pk=obj.vehicle_sold.id, user=request.user)
                car.status = "Sold"
                car.save()

                # Create Contract if it doesn't exist, create it automatically
                if not Contract.objects.filter(vehicle_sold=obj.vehicle_sold, user=request.user).exists():
                    Contract.objects.create(
                        customer_name=obj.lead.name,
                        vehicle_sold=obj.vehicle_sold,
                        price_sold=obj.vehicle_sold.selling_price if obj.vehicle_sold.selling_price else 0,
                        user=request.user
                    )

        obj.save()
        return redirect('sales')

    return render(request, 'update_sell.html', {'form': form})

@login_required
def update_contract(request, id_contract):
    contract = get_object_or_404(Contract, pk=id_contract, user=request.user)
    if request.method == 'GET':
        form = ContractForm(instance=contract)
        form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'update_contract.html', {'form': form})
    form = ContractForm(request.POST, request.FILES, instance=contract)
    form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('contract')
    return render(request, 'update_contract.html', {'form': form})

def aboutus(request):
    return render(request, 'aboutus.html')

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

#View for the contact form

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        full_message = f"Message from: {name} ({email})\n\nSubject: {subject}\n\nMessage:\n{message}"
        
        try:
            # Dealer email where messages will be received
            dealer_email = getattr(settings, 'EMAIL_HOST_USER', 'your_email@gmail.com')
            
            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=full_message,
                from_email=email,
                recipient_list=[dealer_email],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully. We will get back to you shortly!')
        except Exception as e:
            messages.error(request, f'There was an error sending your message: {str(e)}. Please configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py.')
            
        return redirect('contact')
        
    return render(request, 'contact.html')

