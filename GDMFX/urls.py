from django.urls import path
from . import views



urlpatterns =[
    path('', views.home, name = 'home'),
    path('contract', views.contract, name='contract'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory', views.inventory, name='inventory'),
    path('inventory_new', views.new_vehicle, name='new_vehicle'),
    path('inventory_update/<int:id_vehicle>', views.update_vehicle, name='update_vehicle'),
    path('delete_vehicle_image/<int:image_id>', views.delete_vehicle_image, name='delete_vehicle_image'),
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
    path('settings/', views.user_settings, name='user_settings'),
    path('manage_users/', views.manage_users, name='manage_users'),
    #creating the links for update: 
    # path('update_lead/<int:id_lead>', views.update_lead, name='update_lead'),
    
    # --- Blog / Announcement URLs ---
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/post/manage/', views.manage_posts, name='manage_posts'),
    path('blog/post/new/', views.create_post, name='create_post'),
    path('blog/post/<int:post_id>/update/', views.update_post, name='update_post'),
    path('blog/post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('blog/post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('blog/comment/<int:comment_id>/react/', views.react_comment, name='react_comment'),
    path('blog/dealer/post/<int:post_id>/', views.dealer_post_detail, name='dealer_post_detail'),
    path('blog/dealer/comment/<int:comment_id>/reply/', views.dealer_reply, name='dealer_reply'),
]
