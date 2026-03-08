from django.urls import path
from . import views



urlpatterns =[
    path('', views.home, name = 'home'),
    path('contract', views.contract, name='contract'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory', views.inventory, name='inventory'),
    path('inventory_new', views.new_vehicle, name='new_vehicle'),
    path('inventory_update/<int:id_vehicle>', views.update_vehicle, name='update_vehicle'),
    path('leads', views.leads, name='leads'),
    path('leads_new', views.new_lead, name='new_lead'),
    path('leads_update/<int:id_lead>', views.update_lead, name='update_lead'),
    path('login', views.login_page, name='login'),
    path('meets', views.meets, name='meets'),
    path('reports', views.reports, name='reports'),
    path('sales', views.sales, name='sales'),
    path('sales_new', views.new_sale, name='new_sale'),
    path('sales_update/<int:id_sale>', views.update_sale, name='update_sale'),
    path('show_details/<int:id_details>', views.show_details, name='show_details'),
    path('show_contact/<int:id_contract>', views.show_contract, name='show_contract'),
    path('contract_update/<int:id_contract>', views.update_contract, name='update_contract'),
    path('show_sales/<int:id_sales>', views.show_sales, name='show_sales'),
    path('show_lead/<int:id_lead>', views.show_lead, name='show_lead'),
    path('show_forms/<int:id_forms>', views.show_forms, name='show_forms'),
    path('contract_new', views.new_contract, name='new_contract'),
    path('upload_contract_pdf/<int:id_contract>', views.upload_contract_pdf, name='upload_contract_pdf'),
    path('signup', views.signup_page, name='signup'),
    path('logout', views.signout, name='logout'),
    path('appt', views.appt, name='appt'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('contact/', views.contact_view, name='contact'),
    #creating the links for update: 
    # path('update_lead/<int:id_lead>', views.update_lead, name='update_lead'),
]
