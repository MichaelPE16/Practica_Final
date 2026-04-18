from django.contrib import admin
from .models import Vehicles, Leads, Contract, Sales, Meets, VehicleImage, UserProfile, BlogPost, PostImage, PostComment


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

class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle')

admin.site.register(VehicleImage, VehicleImageAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')

admin.site.register(UserProfile, UserProfileAdmin)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_date')

admin.site.register(BlogPost, BlogPostAdmin)

class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post')

admin.site.register(PostImage, PostImageAdmin)

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author_email', 'created_at')

admin.site.register(PostComment, PostCommentAdmin)
