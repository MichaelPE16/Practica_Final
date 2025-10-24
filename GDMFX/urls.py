from django.urls import path
from . import views



urlpatterns =[
    path('', views.home, name = 'home'),
    path('contract', views.contract, name='contract'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory', views.inventory, name='inventory'),
    path('leads', views.leads, name='leads'),
    path('login', views.login_page, name='login'),
    path('meets', views.meets, name='meets'),
    path('reports', views.reports, name='reports'),
    path('sales', views.sales, name='sales'),
    path('show_details', views.show_details, name='show_details'),
    path('show_forms', views.show_forms, name='show_forms'),
    path('signup', views.signup_page, name='signup'),
]

