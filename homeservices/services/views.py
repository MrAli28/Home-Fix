from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, Booking, ServiceArea, Review, Provider
from .forms import BookingForm, UserRegistrationForm, UserProfileForm, ReviewForm


class SmartLoginView(LoginView):
    """Custom login view that redirects admin to admin dashboard, others to their dashboard."""
    template_name = 'services/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/admin-dashboard/'
        # Check if the user is a provider
        try:
            if user.provider_profile and user.provider_profile.is_approved:
                return '/provider/dashboard/'
        except Exception:
            pass
        return '/dashboard/'


class ProviderLoginView(LoginView):
    """Dedicated login view for providers — always redirects to provider dashboard."""
    template_name = 'services/provider_login.html'

    def get_success_url(self):
        user = self.request.user
        # Admin trying to login via provider page — send to admin dashboard
        if user.is_staff or user.is_superuser:
            return '/admin-dashboard/'
        # Check provider profile
        try:
            provider = user.provider_profile
            if provider.is_approved:
                return '/provider/dashboard/'
            else:
                return '/provider/pending/'
        except Exception:
            pass
        # Not a provider — send to customer dashboard
        return '/dashboard/'


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

def service_request(request, service_id):
    """New view for requesting a service and picking area/time"""
    service = get_object_or_404(Service, id=service_id)
    service_areas = _safe_service_areas_queryset()
    return render(request, 'services/service_request.html', {
        'service': service,
        'service_areas': service_areas,
    })

def providers_list(request):
    """Providers listing page based on location and service"""
    service_id = request.GET.get('service')
    location   = request.GET.get('location')
    time_val   = request.GET.get('time')
    date_val   = request.GET.get('date')

    base_qs = Provider.objects.filter(is_approved=True).prefetch_related(
        'user', 'service_types', 'service_areas'
    )
    service_obj = None

    if service_id:
        base_qs = base_qs.filter(service_types__id=service_id)
        service_obj = get_object_or_404(Service, id=service_id)
    if location:
        base_qs = base_qs.filter(service_areas__city__iexact=location)

    # Order all filtered providers
    all_filtered = base_qs.order_by('-rating', '-total_jobs')
    
    # Split into Top 3 and the rest
    top3_providers = all_filtered[:3]
    other_providers = all_filtered[3:]

    return render(request, 'services/providers_list.html', {
        'top3_providers':         top3_providers,
        'other_providers':        other_providers,
        'selected_service':        service_id,
        'selected_location':       location,
        'selected_time':           time_val,
        'selected_date':           date_val,
        'service_obj':             service_obj,
    })


def provider_detail(request, provider_id):
    """Provider detail page"""
    provider = get_object_or_404(Provider, id=provider_id)
    reviews = Review.objects.filter(booking__provider=provider).order_by('-date')
    return render(request, 'services/provider_detail.html', {
        'provider': provider,
        'reviews': reviews,
    })

def contact(request):
    """Contact page view"""
    services = _safe_services_queryset()  # Pass services for the dropdown in contact form
    return render(request, 'services/contact.html', {'services': services})

def book_service(request, service_id=None, provider_id=None):
    """Booking form page"""
    service = None
    provider = None
    
    if not service_id and request.GET.get('service'):
        service_id = request.GET.get('service')

    if service_id:
        service = get_object_or_404(Service, id=service_id)
        
    # provider_id could be passed as query param or URL param.
    # Let's also check GET params if not in URL
    if not provider_id and request.GET.get('provider'):
        provider_id = request.GET.get('provider')
        
    if provider_id:
        provider = get_object_or_404(Provider, id=provider_id)
    
    # If no service passed explicitly, auto-pick from provider's service types
    if not service and provider:
        service = provider.service_types.first()

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
            booking.provider = provider
            booking.status = 'pending'  # Status: pending until admin confirms
            booking.save()
            # Store booking ID in session for the success page
            request.session['booking_id'] = booking.id

            # ── Email to Customer ──
            customer_email = booking.email
            if customer_email:
                provider_name = str(booking.provider) if booking.provider else 'Our Team'
                customer_subject = 'HomeFix – We Received Your Booking Request!'
                customer_message = f"""Dear {booking.customer.get_full_name() if booking.customer else 'Customer'},

Thank you for choosing HomeFix! We have successfully received your service request.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BOOKING DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Booking ID   : #{booking.id}
  Service      : {booking.service.name}
  Date         : {booking.date.strftime('%d %B %Y')}
  Time         : {booking.time.strftime('%I:%M %p')}
  Address      : {booking.address}, {booking.postcode or ''}
  Provider     : {provider_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Our provider or team will contact you shortly to confirm your appointment.

If you have any questions, feel free to reply to this email.

Warm Regards,
The HomeFix Team
thehomefixuk@gmail.com
"""
                try:
                    send_mail(customer_subject, customer_message, settings.DEFAULT_FROM_EMAIL, [customer_email], fail_silently=True)
                except Exception:
                    pass

            # ── Email to Provider ──
            if booking.provider and booking.provider.user.email:
                provider_subject = f'HomeFix – New Booking Request #{booking.id}'
                provider_message = f"""Hello {booking.provider.user.get_full_name()},

You have received a new booking request on HomeFix. Please review the customer details below and contact them as soon as possible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CUSTOMER DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Name         : {booking.customer.get_full_name() if booking.customer else 'Guest'}
  Email        : {booking.email or 'Not provided'}
  Phone        : {booking.phone_number or 'Not provided'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BOOKING DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Booking ID   : #{booking.id}
  Service      : {booking.service.name}
  Date         : {booking.date.strftime('%d %B %Y')}
  Time         : {booking.time.strftime('%I:%M %p')}
  Address      : {booking.address}, {booking.postcode or ''}
  Notes        : {booking.notes or 'None'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please log in to your HomeFix Provider Dashboard to manage this booking.

The HomeFix Team
"""
                try:
                    send_mail(provider_subject, provider_message, settings.DEFAULT_FROM_EMAIL, [booking.provider.user.email], fail_silently=True)
                except Exception:
                    pass

            return redirect('booking_success')
    else:
        initial_data = {}
        if service:
            initial_data['service'] = service
        # If provider has specific services, we could preselect one, but let's keep it simple
        
        # Pre-fill email from user account if logged in
        if request.user.is_authenticated and request.user.email:
            initial_data['email'] = request.user.email
        form = BookingForm(initial=initial_data)
    
    return render(request, 'services/book.html', {
        'form': form,
        'service': service,
        'provider': provider,
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
        pending_providers = Provider.objects.filter(is_approved=False).order_by('-user__date_joined')
        is_admin = True
    else:
        # Regular user view - show only their bookings
        bookings = Booking.objects.filter(customer=user).order_by('-created_at')
        all_bookings = Booking.objects.none()
        upcoming_bookings = bookings.filter(status__in=['pending', 'confirmed', 'in_progress'])
        past_bookings = bookings.filter(status__in=['completed', 'cancelled'])
        admin_stats = None
        pending_providers = None
        is_admin = False
    
    return render(request, 'services/dashboard.html', {
        'user': user,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'all_bookings': all_bookings,
        'admin_stats': admin_stats,
        'pending_providers': pending_providers,
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
            
            # Update provider rating
            if booking.provider:
                from django.db.models import Avg
                provider = booking.provider
                avg_rating = Review.objects.filter(booking__provider=provider).aggregate(Avg('rating'))['rating__avg']
                if avg_rating is not None:
                    provider.rating = round(avg_rating, 2)
                    provider.save()
            
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


# ─── Provider Flow Views ───────────────────────────────────────────────────────

from .forms import ProviderSignupForm, ProviderProfileForm, ProviderUpdateProfileForm

def provider_signup(request):
    """2-step provider registration: account + service details"""
    if request.method == 'POST':
        step = request.POST.get('step', '1')

        if step == '1':
            user_form = ProviderSignupForm(request.POST)
            profile_form = ProviderProfileForm()
            if user_form.is_valid():
                # Store step 1 data in session
                request.session['provider_signup'] = {
                    'first_name': user_form.cleaned_data['first_name'],
                    'last_name': user_form.cleaned_data['last_name'],
                    'username': user_form.cleaned_data['username'],
                    'email': user_form.cleaned_data['email'],
                    'password': user_form.cleaned_data['password1'],
                }
                return render(request, 'services/provider_signup.html', {
                    'step': 2,
                    'user_form': user_form,
                    'profile_form': ProviderProfileForm(),
                })
            return render(request, 'services/provider_signup.html', {
                'step': 1,
                'user_form': user_form,
                'profile_form': ProviderProfileForm(),
            })

        elif step == '2':
            signup_data = request.session.get('provider_signup')
            if not signup_data:
                messages.error(request, 'Session expired. Please start again.')
                return redirect('provider_signup')

            profile_form = ProviderProfileForm(request.POST)
            if profile_form.is_valid():
                # Create user
                user = User.objects.create_user(
                    username=signup_data['username'],
                    email=signup_data['email'],
                    password=signup_data['password'],
                    first_name=signup_data['first_name'],
                    last_name=signup_data['last_name'],
                )
                # Create provider (not approved yet)
                provider = Provider.objects.create(
                    user=user,
                    phone=profile_form.cleaned_data['phone'],
                    experience=profile_form.cleaned_data['experience'],
                    bio=profile_form.cleaned_data['bio'],
                    is_approved=False,
                )
                provider.service_types.set(profile_form.cleaned_data['service_types'])
                provider.service_areas.set(profile_form.cleaned_data['service_areas'])

                del request.session['provider_signup']
                messages.success(request, 'Registration submitted! You will receive an email once approved.')
                return redirect('provider_pending')
            
            return render(request, 'services/provider_signup.html', {
                'step': 2,
                'profile_form': profile_form,
            })
    else:
        user_form = ProviderSignupForm()
        profile_form = ProviderProfileForm()

    return render(request, 'services/provider_signup.html', {
        'step': 1,
        'user_form': user_form,
        'profile_form': profile_form,
    })


def provider_pending(request):
    """Page shown after provider submits signup, waiting for admin approval"""
    return render(request, 'services/provider_pending.html')


@login_required
def admin_approve_provider(request, provider_id):
    """Approve provider from the admin front-end dashboard"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
        
    provider = get_object_or_404(Provider, id=provider_id)
    if request.method == 'POST':
        provider.is_approved = True
        provider.save()
        
        from django.core.mail import send_mail
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
                fail_silently=False,
            )
            messages.success(request, f'{provider.user.get_full_name()} has been approved and notified by email!')
        except Exception as e:
            messages.warning(request, f'{provider.user.get_full_name()} was approved, but the email failed to send: {e}')
            
    return redirect('dashboard')


@login_required
def provider_dashboard(request):
    """Provider's personal dashboard"""
    try:
        provider = request.user.provider_profile
    except Provider.DoesNotExist:
        messages.error(request, 'You do not have a provider profile.')
        return redirect('home')

    if not provider.is_approved:
        return redirect('provider_pending')

    bookings = Booking.objects.filter(provider=provider).order_by('-created_at')
    reviews = Review.objects.filter(booking__provider=provider).order_by('-date')

    return render(request, 'services/provider_dashboard.html', {
        'provider': provider,
        'bookings': bookings,
        'reviews': reviews,
    })


@login_required
def provider_update_profile(request):
    """Provider updates their own bio, experience, areas"""
    try:
        provider = request.user.provider_profile
    except Provider.DoesNotExist:
        return redirect('home')

    if not provider.is_approved:
        return redirect('provider_pending')

    if request.method == 'POST':
        form = ProviderUpdateProfileForm(request.POST)
        if form.is_valid():
            provider.phone = form.cleaned_data['phone']
            provider.experience = form.cleaned_data['experience']
            provider.bio = form.cleaned_data['bio']
            provider.service_areas.set(form.cleaned_data['service_areas'])
            provider.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('provider_dashboard')
    else:
        form = ProviderUpdateProfileForm(initial={
            'phone': provider.phone,
            'experience': provider.experience,
            'bio': provider.bio,
            'service_areas': provider.service_areas.all(),
        })

    return render(request, 'services/provider_update_profile.html', {
        'form': form,
        'provider': provider,
    })


@login_required
def provider_update_booking(request, booking_id):
    """Provider updates status of a booking assigned to them"""
    try:
        provider = request.user.provider_profile
    except Provider.DoesNotExist:
        return redirect('home')

    if not provider.is_approved:
        return redirect('provider_pending')

    booking = get_object_or_404(Booking, id=booking_id, provider=provider)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = [s[0] for s in Booking.STATUS_CHOICES]
        if new_status in valid_statuses:
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking #{booking.id} updated to {new_status.replace("_"," ").title()}.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('provider_dashboard')

