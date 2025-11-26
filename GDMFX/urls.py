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
    path('show_details/<int:id_details>', views.show_details, name='show_details'),
    path('show_contact/<int:id_contract>', views.show_contract, name='show_contract'),
    path('show_sales/<int:id_sales>', views.show_sales, name='show_sales'),
    path('show_lead/<int:id_lead>', views.show_lead, name='show_lead'),
    path('show_forms/<int:id_forms>', views.show_forms, name='show_forms'),
    path('upload_contract_pdf/<int:id_contract>', views.upload_contract_pdf, name='upload_contract_pdf'),
    path('signup', views.signup_page, name='signup'),
    path('logout', views.signout, name='logout'),
]

