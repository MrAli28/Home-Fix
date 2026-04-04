from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.db.utils import OperationalError, ProgrammingError
from .models import Service, Booking, ServiceArea, Review
from .forms import BookingForm, UserRegistrationForm, UserProfileForm, ReviewForm


def _safe_services_queryset():
    try:
        return Service.objects.all()
    except (OperationalError, ProgrammingError):
        return Service.objects.none()


def _safe_service_areas_queryset():
    try:
        return ServiceArea.objects.all()
    except (OperationalError, ProgrammingError):
        return ServiceArea.objects.none()

def home(request):
    """Home page view"""
    services = _safe_services_queryset()
    service_areas = _safe_service_areas_queryset()
    return render(request, 'services/home.html', {
        'services': services,
        'service_areas': service_areas,
    })

def about(request):
    """About page view"""
    return render(request, 'services/about.html')

def privacy_policy(request):
    """Privacy policy page view"""
    return render(request, 'services/privacy_policy.html')

def terms_of_service(request):
    """Terms of service page view"""
    return render(request, 'services/terms_of_service.html')

def services_list(request):
    """Services listing page"""
    services = _safe_services_queryset()
    return render(request, 'services/services.html', {'services': services})

def service_detail(request, service_id):
    """Service detail page"""
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'services/service_detail.html', {
        'service': service,
    })

def contact(request):
    """Contact page view"""
    services = _safe_services_queryset()  # Pass services for the dropdown in contact form
    return render(request, 'services/contact.html', {'services': services})

def book_service(request, service_id=None):
    """Booking form page"""
    service = None
    if service_id:
        service = get_object_or_404(Service, id=service_id)
    
    # Get all services for the dropdown
    services = _safe_services_queryset()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # Associate with user if logged in
            if request.user.is_authenticated:
                booking.customer = request.user
                # Pre-fill email from user account if not provided
                if not booking.email and request.user.email:
                    booking.email = request.user.email
            # Customer books directly without a provider assignment stage.
            booking.provider = None
            booking.status = 'pending'  # Status: pending until admin confirms
            booking.save()
            # Store booking ID in session for the success page
            request.session['booking_id'] = booking.id
            return redirect('booking_success')
    else:
        initial_data = {}
        if service:
            initial_data['service'] = service
        # Pre-fill email from user account if logged in
        if request.user.is_authenticated and request.user.email:
            initial_data['email'] = request.user.email
        form = BookingForm(initial=initial_data)
    
    return render(request, 'services/book.html', {
        'form': form,
        'service': service,
        'services': services,
    })

def booking_success(request):
    """Booking success page"""
    booking_id = request.session.get('booking_id')
    booking = None
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)
    
    return render(request, 'services/booking_success.html', {
        'booking': booking
    })

@login_required
def dashboard(request):
    """User dashboard view"""
    user = request.user
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    
    # Admin can see all bookings, regular users only see their own
    if user.is_staff or user.is_superuser:
        # Admin view - show all bookings
        bookings = Booking.objects.select_related('customer', 'service').all().order_by('-created_at')

        if search_query:
            bookings = bookings.filter(
                Q(service__name__icontains=search_query)
                | Q(customer__username__icontains=search_query)
                | Q(customer__first_name__icontains=search_query)
                | Q(customer__last_name__icontains=search_query)
                | Q(phone_number__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(address__icontains=search_query)
                | Q(postcode__icontains=search_query)
            )

        valid_statuses = [choice[0] for choice in Booking.STATUS_CHOICES]
        if status_filter and status_filter in valid_statuses:
            bookings = bookings.filter(status=status_filter)

        if date_from:
            bookings = bookings.filter(date__gte=date_from)
        if date_to:
            bookings = bookings.filter(date__lte=date_to)

        all_bookings = bookings.order_by('-date', '-time', '-created_at')
        upcoming_bookings = bookings.filter(status__in=['pending', 'confirmed', 'in_progress'])
        past_bookings = bookings.filter(status__in=['completed', 'cancelled'])
        admin_stats = {
            'total': bookings.count(),
            'in_progress': bookings.filter(status='in_progress').count(),
            'completed': bookings.filter(status='completed').count(),
            'cancelled': bookings.filter(status='cancelled').count(),
        }
        is_admin = True
    else:
        # Regular user view - show only their bookings
        bookings = Booking.objects.filter(customer=user).order_by('-created_at')
        all_bookings = Booking.objects.none()
        upcoming_bookings = bookings.filter(status__in=['pending', 'confirmed', 'in_progress'])
        past_bookings = bookings.filter(status__in=['completed', 'cancelled'])
        admin_stats = None
        is_admin = False
    
    return render(request, 'services/dashboard.html', {
        'user': user,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'all_bookings': all_bookings,
        'admin_stats': admin_stats,
        'is_admin': is_admin,
        'filters': {
            'q': search_query,
            'status': status_filter,
            'date_from': date_from,
            'date_to': date_to,
        },
    })

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if request.method == 'POST':
        if booking.status not in ['pending', 'confirmed']:
            messages.error(request, 'Only pending or confirmed bookings can be cancelled.')
            return redirect('dashboard')
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully')
        return redirect('dashboard')
    
    return render(request, 'services/cancel_booking.html', {'booking': booking})

@login_required
def rate_booking(request, booking_id):
    """Rate a completed booking"""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user, status='completed')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            
            # Update booking with rating
            booking.rating = review.rating
            booking.feedback = review.comment
            booking.save()
            
            messages.success(request, 'Thank you for your review!')
            return redirect('dashboard')
    else:
        form = ReviewForm()
    
    return render(request, 'services/rate_booking.html', {
        'booking': booking,
        'form': form,
    })

@login_required
def update_booking_status(request, booking_id, status):
    """Update booking status - admin only"""
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('dashboard')

    # Check if user is admin
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('dashboard')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Validate the status
    valid_statuses = [status_choice[0] for status_choice in Booking.STATUS_CHOICES]
    if status not in valid_statuses:
        messages.error(request, f"Invalid status: {status}")
        return redirect('dashboard')
    
    # Update the booking status
    booking.status = status
    booking.save()
    
    messages.success(request, f"Booking #{booking_id} status updated to {status.replace('_', ' ').title()}")
    return redirect('dashboard')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend when logging in the user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'services/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'services/profile.html', {'form': form})

def check_postcode(request):
    """AJAX view to check if a postcode is in service area"""
    postcode = request.GET.get('postcode', '')
    if not postcode:
        return JsonResponse({'valid': False})
    
    # Check if postcode is in any service area
    service_areas = ServiceArea.objects.all()
    for area in service_areas:
        postcodes = area.get_postcodes_list()
        for code in postcodes:
            if postcode.upper().startswith(code.upper()):
                return JsonResponse({'valid': True, 'area': area.city})
    
    return JsonResponse({'valid': False})
