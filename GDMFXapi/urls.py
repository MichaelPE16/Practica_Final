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

    path('blogs/', views.blogs_list, name='blogs-list'),
    path('blogs/<int:pk>/', views.blogs_detail, name='blogs-detail'),

    path('postimages/', views.postimages_list, name='postimages-list'),
    path('postimages/<int:pk>/', views.postimages_detail, name='postimages-detail'),

    path('postcomments/', views.postcomments_list, name='postcomments-list'),
    path('postcomments/<int:pk>/', views.postcomments_detail, name='postcomments-detail'),
]
