from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewall, name='viewall'),
    path('leads/', views.leads_list, name='leads-list'),
    path('leads/<int:pk>/', views.leads_detail, name='leads-detail'),

    path('vehicles/', views.vehicles_list, name='vehicles-list'),
    path('vehicles/<int:pk>/', views.vehicles_detail, name='vehicles-detail'),

    path('contracts/', views.contracts_list, name='contracts-list'),
    path('contracts/<int:pk>/', views.contracts_detail, name='contracts-detail'),

    path('meets/', views.meets_list, name='meets-list'),
    path('meets/<int:pk>/', views.meets_detail, name='meets-detail'),

    path('sales/', views.sales_list, name='sales-list'),
    path('sales/<int:pk>/', views.sales_detail, name='sales-detail'),
]
