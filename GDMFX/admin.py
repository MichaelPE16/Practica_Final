from django.contrib import admin
from .models import Vehicles, Leads, Contract, Sales


class VehicleAdmin(admin.ModelAdmin): 
    list_display = ('id', 'vin', 'user')

admin.site.register(Vehicles, VehicleAdmin)
class LeadAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'user')

admin.site.register(Leads, LeadAdmin)




