from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    """Model for different types of services offered"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Store icon name/class
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Provider(models.Model):
    """Model for service providers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    service_types = models.ManyToManyField(Service)
    experience = models.TextField()
    bio = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    total_jobs = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Booking(models.Model):
    """Model for service bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, related_name='provider_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    def __str__(self):
        service_name = self.service.name if self.service else "Unknown Service"
        return f"Booking #{self.id} - {service_name}"

class Review(models.Model):
    """Model for service reviews"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.booking.service.name} by {self.booking.customer.username}"

class ServiceArea(models.Model):
    """Model for service coverage areas"""
    city = models.CharField(max_length=100)
    postcodes = models.TextField(help_text="Comma separated list of postcodes")
    
    def __str__(self):
        return self.city
    
    def get_postcodes_list(self):
        return [code.strip() for code in self.postcodes.split(',')]
