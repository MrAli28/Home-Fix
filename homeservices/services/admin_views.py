from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
from .models import Service, Provider, Booking, Review, ServiceArea
from django.core.mail import send_mail

# Decorator to ensure only admin can access these views
def admin_required(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@user_passes_test(admin_required, login_url='login')
def admin_dashboard_home(request):
    """Main overview for the custom admin dashboard"""
    # Calculate stats
    total_customers = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_providers = Provider.objects.filter(is_approved=True).count()
    pending_providers = Provider.objects.filter(is_approved=False).count()
    
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.filter(status='completed').aggregate(total=Sum('price'))['total'] or 0
    
    # Recent activity
    recent_bookings = Booking.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_customers': total_customers,
        'total_providers': total_providers,
        'pending_providers': pending_providers,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'recent_users': recent_users,
        'active_tab': 'dashboard',
    }
    return render(request, 'admin_dashboard/admin_home.html', context)


@user_passes_test(admin_required, login_url='login')
def admin_manage_users(request):
    """Manage standard customers"""
    query = request.GET.get('q', '')
    users = User.objects.filter(is_staff=False, is_superuser=False, provider_profile__isnull=True).order_by('-date_joined')
    
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
        
    context = {
        'users': users,
        'search_query': query,
        'active_tab': 'users',
    }
    return render(request, 'admin_dashboard/admin_users.html', context)


@user_passes_test(admin_required, login_url='login')
def admin_manage_providers(request):
    """Manage service providers"""
    query = request.GET.get('q', '')
    providers = Provider.objects.all().order_by('-user__date_joined')
    
    if query:
        providers = providers.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
        
    pending = providers.filter(is_approved=False)
    active = providers.filter(is_approved=True)
    
    context = {
        'pending_providers': pending,
        'active_providers': active,
        'search_query': query,
        'active_tab': 'providers',
    }
    return render(request, 'admin_dashboard/admin_providers.html', context)


@user_passes_test(admin_required, login_url='login')
def admin_approve_provider(request, provider_id):
    """Action to approve or suspend a provider"""
    provider = get_object_or_404(Provider, id=provider_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            provider.is_approved = True
            provider.save()
            try:
                send_mail(
                    subject='🎉 Your HomeFix Provider Account Has Been Approved!',
                    message=(
                        f"Hi {provider.user.first_name},\n\n"
                        "Great news! Your application to join HomeFix as a service provider has been approved.\n\n"
                        "You can now log in to your provider dashboard to manage bookings.\n\n"
                        "— The HomeFix Team"
                    ),
                    from_email=None,
                    recipient_list=[provider.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, f'Provider {provider.user.get_full_name()} approved successfully.')
            
        elif action == 'suspend':
            provider.is_approved = False
            provider.save()
            messages.warning(request, f'Provider {provider.user.get_full_name()} suspended.')
            
    return redirect('admin_manage_providers')


@user_passes_test(admin_required, login_url='login')
def admin_manage_bookings(request):
    """Manage all bookings"""
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    
    bookings = Booking.objects.all().order_by('-created_at')
    
    if query:
        bookings = bookings.filter(
            Q(customer__username__icontains=query) |
            Q(provider__user__username__icontains=query) |
            Q(service__name__icontains=query)
        )
    if status:
        bookings = bookings.filter(status=status)
        
    context = {
        'bookings': bookings,
        'search_query': query,
        'current_status': status,
        'status_choices': Booking.STATUS_CHOICES,
        'active_tab': 'bookings',
    }
    return render(request, 'admin_dashboard/admin_bookings.html', context)


@user_passes_test(admin_required, login_url='login')
def admin_update_booking_status(request, booking_id):
    """Action to update a booking status"""
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = [s[0] for s in Booking.STATUS_CHOICES]
        if new_status in valid_statuses:
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking #{booking.id} updated to {new_status}.')
    return redirect('admin_manage_bookings')


@user_passes_test(admin_required, login_url='login')
def admin_manage_website(request):
    """Manage Services and Areas"""
    services = Service.objects.all().order_by('category', 'name')
    areas = ServiceArea.objects.all().order_by('city')
    
    context = {
        'services': services,
        'areas': areas,
        'active_tab': 'website',
    }
    return render(request, 'admin_dashboard/admin_website.html', context)
