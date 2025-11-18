from .models import Sales, Contract, Leads, Vehicles
from django.forms import ModelForm
from django import forms



class SalesForm(ModelForm): 
    class Meta: 
        model = Sales
        fields = ['lead', 'vehicle_sold', 'phase', 'selling_date', 'user']
        widgets = {
            'lead':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Lead Name' }),
            'vehicle_sold':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark' }), 
            'phase':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark' }), 
            'selling_date': forms.DateInput,
            'user':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark' })
        }

class ContractForm(ModelForm): 
    class Meta: 
        model = Contract
        fields = ['customer_name', 'id_document', 'email', 'phone', 'address', 'vehicle_sold', 'price_sold', 'sign_date', 'received', 'file_pdf', 'customer_type', 'user']
        widgets = {
            'customer_name':forms.TextInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Customer Name' }),
            'id_document': forms.TextInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'GOV ID' }), 
            'email':forms.EmailInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Email' }), 
            'phone':forms.NumberInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Phone number' }), 
            'address':forms.Textarea(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Address' }), 
            'vehicle_sold':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark '}), 
            'price_sold': forms.NumberInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark', 'placeholder': 'Price Sold'}),
            'sign_date': forms.DateInput(attrs={'class': 'form-control bg-transparent border-info text-bg-dark'}),
            'received': forms.DateInput(attrs={'class': 'form-control bg-transparent border-info text-bg-dark'}),
            'file_pdf': forms.FileField,
            'customer_type':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark '}), 
            'user':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark' })
        }


class LeadsForm(ModelForm): 
    class Meta: 
        model = Leads
        fields = ['name', 'interested', 'source', 'status', 'contact_date', 'bullet', 'user']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Lead Name' }),
            'interested': forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark '}), 
            'source':forms.Textarea(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'How you find about us...' }), 
            'status':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark' }), 
            'contact_date': forms.DateTimeInput(attrs={'class': 'form-control bg-transparent border-info text-bg-dark'}), 
            'bullet': forms.NumberInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark', 'placeholder': 'Bullet'}),
            'user':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark '})
        }


class VehicleForm(ModelForm): 
    class Meta: 
        model = Vehicles
        fields = ['vin', 'brand', 'model', 'condition', 'km', 'color', 'price_adquisition', 'selling_price', 'integration_date', 'status', 'user']
        widgets = {
            'vin':forms.TextInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Vehicule Unique Number' }),
            'brand': forms.TextInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Honda...' }), 
            'model':forms.TextInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Civic...' }), 
            'condition':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark '}), 
            'km': forms.NumberInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': '155 Km' }),
            'color': forms.TextInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark ', 'PlaceHolder': 'Vehicule Color' }),
            'price_adquisition': forms.NumberInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark', 'placeholder': 'Price Adquisition'}),
            'selling_price': forms.NumberInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark', 'placeholder': 'Selling Price'}),
            'integration_date': forms.DateInput(attrs={'class':'form-control bg-transparent border-info text-bg-dark' }),
            'status':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark ' }),  
            'user':forms.Select(attrs={'class':'form-control bg-transparent border-info text-bg-dark' })
        }
