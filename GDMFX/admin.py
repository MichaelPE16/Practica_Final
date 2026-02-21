from django.contrib import admin
from .models import Vehicles, Leads, Contract, Sales, Meets


class VehicleAdmin(admin.ModelAdmin): 
    list_display = ('id', 'vin', 'user')

admin.site.register(Vehicles, VehicleAdmin)

class LeadAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'user')

admin.site.register(Leads, LeadAdmin)

class ContactAdmin(admin.ModelAdmin): 
    list_display = ('id', 'customer_name', 'user')

admin.site.register(Contract, ContactAdmin)

class SalesAdmin(admin.ModelAdmin): 
    list_display = ('id', 'lead', 'user')

admin.site.register(Sales, SalesAdmin)

class MeetsAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'user')

admin.site.register(Meets, MeetsAdmin)
