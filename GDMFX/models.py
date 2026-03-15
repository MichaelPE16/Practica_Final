from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Vehicles(models.Model): 
    vin = models.CharField(max_length=17, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    CONDITION_CHOICES = [
        ('Used', 'Used'),
        ('New', 'New'),
    ]
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    km = models.IntegerField(default=0)
    color = models.CharField(max_length=50)
    price_adquisition = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    integration_date = models.DateField(null=True, blank=True)
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.vin
    

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicles, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicle_images/')

    def __str__(self):
        return f"Image for {self.vehicle.vin}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    email_password = models.CharField(max_length=255, blank=True, null=True)
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def is_admin(self):
        return self.role == 'Admin'

    @property
    def is_employee(self):
        return self.role == 'Employee'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'Admin' if instance.is_superuser else 'Employee'
        UserProfile.objects.create(user=instance, role=role)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        role = 'Admin' if instance.is_superuser else 'Employee'
        UserProfile.objects.create(user=instance, role=role)


class Leads(models.Model): 
    name = models.CharField(max_length=150)
    interested = models.ForeignKey(Vehicles, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=150)
    LEAD_STATUS_CHOICES = [
        ('Interested', 'Interested'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
    ]
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='Interested')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contact_date = models.DateTimeField(null=True, blank=True)
    bullet = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name

class Sales(models.Model): 
    lead = models.OneToOneField(Leads, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # References the vehicle that was sold in this sale; can be null if not assigned yet.
    vehicle_sold = models.ForeignKey(Vehicles, on_delete=models.SET_NULL, null=True, blank=True)
    PHASE_CHOICES = [
        ('Test Drive', 'Test Drive'), 
        ('In progress', 'In progress'), 
        ('Closed', 'Closed'),
    ]
    phase = models.CharField(max_length=20, choices=PHASE_CHOICES, default='Test Drive')
    selling_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Sale for {self.lead.name}"


class Contract(models.Model):

    customer_name = models.CharField(max_length=150)
    id_document = models.CharField(max_length=13, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True)
    vehicle_sold = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    price_sold = models.DecimalField(max_digits=12, decimal_places=2)
    sign_date = models.DateField(null=True, blank=True)
    received = models.DateField(null=True, blank=True)
    file_pdf = models.FileField(upload_to='contracts/', null=True, blank=True)
    CUSTOMER_TYPE_CHOICES = [
        ('Customer', 'Customer'),
        ('Business', 'Business'),
    ]
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Contract for {self.customer_name}"
    
class Meets(models.Model):
    message = models.CharField(max_length=150)
    date = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'user')
        verbose_name_plural = "Meetings"

    def __str__(self) -> str:
        return f"Appt for {self.name} on {self.date}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    
    def __str__(self):
        return f"Image for {self.post.title}"

class PostComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author_email = models.EmailField(max_length=254)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_dealer_reply = models.BooleanField(default=False)
    heart_reactions = models.IntegerField(default=0)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author_email} on {self.post.title}"