from django.contrib import admin
from django.core.mail import send_mail
from django.contrib import messages
from .models import Service, Provider, Booking, Review, ServiceArea

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price')
    list_filter = ('category',)
    search_fields = ('name', 'description')


def approve_providers(modeladmin, request, queryset):
    """Admin action: approve selected providers and send them an email notification"""
    approved_count = 0
    for provider in queryset.filter(is_approved=False):
        provider.is_approved = True
        provider.save()
        # Send approval email
        try:
            send_mail(
                subject='🎉 Your HomeFix Provider Account Has Been Approved!',
                message=(
                    f"Hi {provider.user.first_name},\n\n"
                    "Great news! Your application to join HomeFix as a service provider has been approved.\n\n"
                    "You can now log in to your provider dashboard to:\n"
                    "  • View your assigned bookings\n"
                    "  • Update booking statuses\n"
                    "  • Edit your profile and service areas\n\n"
                    "Login at: http://127.0.0.1:8000/login/\n\n"
                    "Welcome to the HomeFix team!\n\n"
                    "— The HomeFix Team"
                ),
                from_email=None,
                recipient_list=[provider.user.email],
                fail_silently=False,
            )
        except Exception as e:
            modeladmin.message_user(
                request,
                f"Provider {provider} approved but email failed: {e}",
                level=messages.WARNING,
            )
            continue
        approved_count += 1

    modeladmin.message_user(request, f"{approved_count} provider(s) approved and notified by email.", messages.SUCCESS)

approve_providers.short_description = "✅ Approve selected providers & send email"


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_email', 'is_approved', 'rating', 'total_jobs')
    list_filter = ('is_approved', 'service_types')
    search_fields = ('user__username', 'user__email', 'bio')
    actions = [approve_providers]

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


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
