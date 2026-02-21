from .models import Sales, Contract, Leads, Vehicles
from django.forms import ModelForm
from django import forms



class SalesForm(ModelForm): 
    class Meta: 
        model = Sales
        fields = ['lead', 'vehicle_sold', 'phase', 'selling_date', 'user']
        widgets = {
            # SELECTS: Usamos text-white para el texto principal y bg-dark para el fondo de Bootstrap
            'lead': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Lead Name'}),
            'vehicle_sold': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            'phase': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            
            # INPUTS: Usamos text-black. Si tu fondo es oscuro, DEBERÍA ser text-white
            # Asumiendo que tu fondo de página es oscuro, cambiamos a text-white para que se vea:
            'selling_date': forms.DateInput(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            'user': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'})
        }

class ContractForm(ModelForm): 
    class Meta: 
        model = Contract
        fields = ['customer_name', 'id_document', 'email', 'phone', 'address', 'vehicle_sold', 'price_sold', 'sign_date', 'received', 'file_pdf', 'customer_type', 'user']
        widgets = {
            # TEXT INPUTS: Cambiamos a text-white asumiendo fondo oscuro
            'customer_name': forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Customer Name'}),
            'id_document': forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'GOV ID'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Email'}), 
            'phone': forms.NumberInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Phone number'}), 
            'address': forms.Textarea(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Address'}), 
            
            # SELECTS: Usamos bg-white y text-dark
            'vehicle_sold': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            
            # INPUTS: Cambiamos a text-white
            'price_sold': forms.NumberInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'placeholder': 'Price Sold'}),
            'sign_date': forms.DateInput(attrs={'class': 'form-control bg-dark border-secondary text-light'}),
            'received': forms.DateInput(attrs={'class': 'form-control bg-dark border-secondary text-light'}),
            'file_pdf': forms.ClearableFileInput(attrs={'class': 'form-control bg-dark border-secondary text-light'}),
            
            # SELECTS: Usamos bg-white y text-dark
            'customer_type': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            'user': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'})
        }


class LeadsForm(ModelForm): 
    class Meta: 
        model = Leads
        fields = ['name', 'interested', 'source', 'status', 'contact_date', 'bullet', 'user']
        widgets = {
            # INPUTS: Cambiamos a text-white
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Lead Name'}),
            'source': forms.Textarea(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'How you find about us...'}), 
            'contact_date': forms.DateTimeInput(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            'bullet': forms.NumberInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'placeholder': 'Bullet'}),
            
            # SELECTS: Usamos bg-dark y text-white
            'interested': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            'status': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            'user': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'})    
        }


class VehicleForm(ModelForm): 
    class Meta: 
        model = Vehicles
        fields = ['vin', 'brand', 'model', 'condition', 'km', 'color', 'price_adquisition', 'selling_price', 'integration_date', 'status', 'user']
        widgets = {
            # INPUTS: Cambiamos a text-white
            'vin': forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Vehicule Unique Number'}),
            'brand': forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Honda...'}), 
            'model': forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Civic...'}), 
            'km': forms.NumberInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': '155 Km'}),
            'color': forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'PlaceHolder': 'Vehicule Color'}),
            'price_adquisition': forms.NumberInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'placeholder': 'Price Adquisition'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'placeholder': 'Selling Price'}),
            'integration_date': forms.DateInput(attrs={'class': 'form-control bg-dark border-secondary text-light'}),
            
            # SELECTS: Usamos bg-white y text-dark
            'condition': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}), 
            'status': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'}),
            'user': forms.Select(attrs={'class': 'form-control bg-dark border-secondary text-light'})
        }
