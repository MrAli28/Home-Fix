from django.contrib import admin
from .models import Service, Provider, Booking, Review, ServiceArea

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'rating', 'total_jobs')
    list_filter = ('service_types',)
    search_fields = ('user__username', 'user__email', 'bio')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'customer', 'provider', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer__username', 'provider__user__username', 'service__name')
    date_hierarchy = 'date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('comment', 'booking__customer__username')

@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('city', 'postcodes')
    search_fields = ('city', 'postcodes')
