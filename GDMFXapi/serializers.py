from rest_framework import serializers
from GDMFX.models import Leads, Vehicles, Contract, Meets, Sales

class LeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'

class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class MeetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meets
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'