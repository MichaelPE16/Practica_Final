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
from django.http import JsonResponse
from .forms import ContractForm, LeadsForm, SalesForm, VehicleForm, Apptform, BlogPostForm
from .models import Contract, Leads, Sales, Vehicles, Meets, BlogPost, PostComment, PostImage, VehicleImage, UserProfile

ITEMS_PER_PAGE = 10

# Create your views here.
def home(request): 
    return render(request, 'home.html')

@login_required
def contract(request): 
    is_admin = request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')
    base_qs = Contract.objects.all() if is_admin else Contract.objects.filter(user=request.user)

    if request.method == "POST": 
        search =request.POST['search']
        idcontact = request.POST['ID']
        contract = base_qs.filter(customer_name__contains = search, id_document__contains =idcontact )
        paginator = Paginator(contract, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'contract.html',{'contracts': page_obj} )
    else: 
        contract = base_qs
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

    is_admin = request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')

    # Base QuerySets (Inventory and Leads: All can see. Sales and Contracts: RBAC)
    sales_qs = Sales.objects.all() if is_admin else Sales.objects.filter(user=request.user)
    contracts_qs = Contract.objects.all() if is_admin else Contract.objects.filter(user=request.user)
    vehicles_qs = Vehicles.objects.all()
    leads_qs = Leads.objects.all()

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
        
    all_brands = Vehicles.objects.values_list('brand', flat=True).distinct()

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
    base_qs = Vehicles.objects.all()

    if request.method == 'POST': 
        search = request.POST['search']
        status = request.POST['status']
        vehicle = base_qs.filter(brand__contains = search, status = status)
        if status == 'All Statuses':
            vehicle = base_qs.filter(brand__contains = search)
        if search == '':
            vehicle = base_qs.filter(status = status)
        if search == '' and status == 'All Statuses':
            vehicle = base_qs.all()
        paginator = Paginator(vehicle, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventory.html',
        {'vehicles': page_obj} )
    else: 
        vehicle = base_qs.all()
    # Pagination
    paginator = Paginator(vehicle, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory.html',
    {'vehicles': page_obj} )

@login_required
def leads(request):
    base_qs = Leads.objects.all()

    if request.method == 'POST':
        search = request.POST['search']
        status = request.POST['status']
        leads = base_qs.filter(name__contains=search, status=status)
        if status == 'All Statuses':
            leads = base_qs.filter(name__contains=search)
        if search == '':
            leads = base_qs.filter(status=status)
        if search == '' and status == 'All Statuses':
            leads = base_qs.all()
        
        paginator = Paginator(leads, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'leads.html', {'leads': page_obj})
    else:
        leads = base_qs.all()
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
    is_admin = request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')
    base_qs = Meets.objects.all() if is_admin else Meets.objects.filter(user=request.user)

    search = request.POST.get('search', '')
    if request.method == 'POST' and search:
        meetings = base_qs.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        ).order_by('-date')
    else:
        meetings = base_qs.order_by('-date')
    
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
    is_admin = request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')
    base_qs = Sales.objects.all() if is_admin else Sales.objects.filter(user=request.user)

    if request.method == "POST": 
        search = request.POST['search']
        if search:
            sale = base_qs.filter(
                Q(lead__name__contains=search) | Q(vehicle_sold__vin__contains=search)
            )
        else:
            sale = base_qs.all()
        paginator = Paginator(sale, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sales.html',{'sales': page_obj} )
    else: 
        sale = base_qs.all()
        # Pagination
        paginator = Paginator(sale, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sales.html',{'sales': page_obj} )

#Este muestra los detalles de un vehiculo
@login_required
def show_details(request, id_details): 
    # All users can see inventory details
    vehicle = get_object_or_404(Vehicles, pk= id_details)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                VehicleImage.objects.create(vehicle=vehicle, image=image)
            messages.success(request, 'Image(s) uploaded successfully.')
        return redirect('show_details', id_details=id_details)

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
    form = VehicleForm(request.POST, request.FILES)
    form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
    if form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.user = request.user
        vehicle.save()
        images = request.FILES.getlist('images')
        for image in images:
            VehicleImage.objects.create(vehicle=vehicle, image=image)
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
    # Depending on RBAC, let's allow all or owner. For now, matching original mostly, but anyone can view inventory, maybe only owner/admin can edit.
    is_admin = request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')
    vehicle = get_object_or_404(Vehicles, pk=id_vehicle) if is_admin else get_object_or_404(Vehicles, pk=id_vehicle, user=request.user)

    if request.method == 'GET':
        form = VehicleForm(instance=vehicle)
        form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
        form.fields['user'].initial = request.user
        return render(request, 'update_inventory.html', {'form': form, 'vehicle': vehicle})
    form = VehicleForm(request.POST, request.FILES, instance=vehicle)
    form.fields['user'].queryset = User.objects.filter(pk = request.user.pk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('inventory')
    return render(request, 'update_inventory.html', {'form': form, 'vehicle': vehicle})

@login_required
def delete_vehicle_image(request, image_id):
    image = get_object_or_404(VehicleImage, id=image_id)
    # Ensure the user deleting the image owns the vehicle
    if image.vehicle.user == request.user or getattr(request.user, 'is_superuser', False) or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin'):
        vehicle_id = image.vehicle.id
        image.delete()
        messages.success(request, 'Image deleted successfully.')
        return redirect('show_details', id_details=vehicle_id)
    return redirect('inventory')

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


# --- Blog / Announcement Views ---

def blog_list(request):
    posts_qs = BlogPost.objects.all().order_by('-publication_date')
    
    # Search by title
    search_query = request.GET.get('search', '')
    if search_query:
        posts_qs = posts_qs.filter(title__icontains=search_query)
        
    # Search by date
    date_query = request.GET.get('date', '')
    if date_query:
        posts_qs = posts_qs.filter(publication_date__date=date_query)

    paginator = Paginator(posts_qs, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'date_query': date_query,
    })

def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if not post.allow_comments:
        return redirect('blog_list')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        content = request.POST.get('content')
        if email and content:
            PostComment.objects.create(
                post=post,
                author_email=email,
                content=content
            )
            messages.success(request, 'Your comment was posted successfully.')
        else:
            messages.error(request, 'Please provide both email and comment content.')
    return redirect('blog_list')

def react_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, id=comment_id)
        comment.heart_reactions += 1
        comment.save()
        return JsonResponse({'success': True, 'hearts': comment.heart_reactions})
    return JsonResponse({'success': False}, status=400)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                PostImage.objects.create(post=post, image=image)
                
            messages.success(request, 'Post created successfully.')
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def manage_posts(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-publication_date')
    return render(request, 'manage_posts.html', {'posts': posts})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    return redirect('manage_posts')

@login_required
def update_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            images = request.FILES.getlist('images')
            if images:
                # Optionally delete old images here if requested, but normally we just append or allow deletion from a separate UI
                # For simplicity, we just append new uploaded ones.
                for image in images:
                    PostImage.objects.create(post=post, image=image)
            messages.success(request, 'Post updated successfully.')
            return redirect('manage_posts')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'update_post.html', {'form': form, 'post': post})

@login_required
def dealer_post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    # Get all top-level comments (not replies)
    comments = post.comments.filter(parent_comment__isnull=True).order_by('-created_at')
    return render(request, 'post_detail_internal.html', {'post': post, 'comments': comments})

@login_required
def dealer_reply(request, comment_id):
    parent_comment = get_object_or_404(PostComment, id=comment_id)
    post = parent_comment.post
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            PostComment.objects.create(
                post=post,
                author_email=request.user.email or request.user.username + "@dealer.com",
                content=content,
                is_dealer_reply=True,
                parent_comment=parent_comment
            )
            messages.success(request, 'Reply posted successfully.')
        else:
            messages.error(request, 'Reply content cannot be empty.')
            
    return redirect('dealer_post_detail', post_id=post.id)

@login_required
def user_settings(request):
    if request.method == 'POST':
        user = request.user
        display_name = request.POST.get('display_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profile_picture')

        try:
            if display_name:
                user.first_name = display_name
            if email:
                user.email = email
            if password:
                user.set_password(password)
                
            if profile_picture:
                user.userprofile.profile_picture = profile_picture
                user.userprofile.save()

            user.save()
            
            if password:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)  # Keep user logged in
            
            messages.success(request, 'Profile updated successfully.')
        except IntegrityError:
            messages.error(request, 'Username already exists. Please choose a different one.')

        return redirect('user_settings')
    
    return render(request, 'user_settings.html')

@login_required
def manage_users(request):
    is_admin = request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')
    if not is_admin:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        target_user = get_object_or_404(User, id=user_id)
        if hasattr(target_user, 'userprofile'):
            target_user.userprofile.role = new_role
            target_user.userprofile.save()
            messages.success(request, f"Updated role for {target_user.username} to {new_role}.")
        return redirect('manage_users')

    users = User.objects.all().select_related('userprofile').order_by('id')
    return render(request, 'manage_users.html', {'users_list': users})
