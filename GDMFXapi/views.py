from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from GDMFX.models import Leads, Vehicles, Contract, Meets, Sales
from .serializers import LeadsSerializer, VehiclesSerializer, ContractSerializer, MeetsSerializer, SalesSerializer


@api_view(['GET'])
def viewall(request):
    if request.method == 'GET':
        leads = Leads.objects.all()
        vehicles = Vehicles.objects.all()
        contracts = Contract.objects.all()
        meets = Meets.objects.all()
        sales = Sales.objects.all()
        serializerLeads = LeadsSerializer(leads, many=True)
        serializerVehicles = VehiclesSerializer(vehicles, many=True)
        serializerContracts = ContractSerializer(contracts, many=True)
        serializerMeets = MeetsSerializer(meets, many=True)
        serializerSales = SalesSerializer(sales, many=True)
        return Response({"leads": serializerLeads.data, "vehicles": serializerVehicles.data, "contracts": serializerContracts.data, "meets": serializerMeets.data, "sales": serializerSales.data})


@api_view(['GET', 'POST'])
def leads_list(request):
    if request.method == 'GET':
        leads = Leads.objects.all()
        serializer = LeadsSerializer(leads, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LeadsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def leads_detail(request, pk):
    try:
        lead = Leads.objects.get(pk=pk)
    except Leads.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LeadsSerializer(lead)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LeadsSerializer(lead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        lead.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def vehicles_list(request):
    if request.method == 'GET':
        vehicles = Vehicles.objects.all()
        serializer = VehiclesSerializer(vehicles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VehiclesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vehicles_detail(request, pk):
    try:
        vehicle = Vehicles.objects.get(pk=pk)
    except Vehicles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = VehiclesSerializer(vehicle)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = VehiclesSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def contracts_list(request):
    if request.method == 'GET':
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def contracts_detail(request, pk):
    try:
        contract = Contract.objects.get(pk=pk)
    except Contract.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ContractSerializer(contract)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ContractSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def meets_list(request):
    if request.method == 'GET':
        meets = Meets.objects.all()
        serializer = MeetsSerializer(meets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MeetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def meets_detail(request, pk):
    try:
        meet = Meets.objects.get(pk=pk)
    except Meets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MeetsSerializer(meet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MeetsSerializer(meet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        meet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def sales_list(request):
    if request.method == 'GET':
        sales = Sales.objects.all()
        serializer = SalesSerializer(sales, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def sales_detail(request, pk):
    try:
        sale = Sales.objects.get(pk=pk)
    except Sales.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SalesSerializer(sale)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SalesSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


