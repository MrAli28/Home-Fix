from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import admin_views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    
    # Providers & Services
    path('service/<int:service_id>/', views.service_request, name='service_request'),
    path('providers/', views.providers_list, name='providers_list'),
    path('providers/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Booking
    path('book/', views.book_service, name='book_service'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('book/provider/<int:provider_id>/', views.book_service, name='book_provider'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/rate/<int:booking_id>/', views.rate_booking, name='rate_booking'),
    path('bookings/update-status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    
    # User account
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.SmartLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='services/password_reset.html',
             email_template_name='services/password_reset_email.html',
             subject_template_name='services/password_reset_subject.txt'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='services/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='services/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='services/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # AJAX endpoints
    path('check-postcode/', views.check_postcode, name='check_postcode'),

    # Provider Flow
    path('provider/login/', views.ProviderLoginView.as_view(), name='provider_login'),
    path('provider/signup/', views.provider_signup, name='provider_signup'),
    path('provider/pending/', views.provider_pending, name='provider_pending'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/profile/edit/', views.provider_update_profile, name='provider_update_profile'),
    path('provider/booking/<int:booking_id>/update/', views.provider_update_booking, name='provider_update_booking'),
    path('admin/provider/<int:provider_id>/approve/', views.admin_approve_provider, name='admin_approve_provider'),

    # New Professional Admin Dashboard
    path('admin-dashboard/', admin_views.admin_dashboard_home, name='admin_dashboard_home'),
    path('admin-dashboard/users/', admin_views.admin_manage_users, name='admin_manage_users'),
    path('admin-dashboard/providers/', admin_views.admin_manage_providers, name='admin_manage_providers'),
    path('admin-dashboard/providers/<int:provider_id>/action/', admin_views.admin_approve_provider, name='admin_dashboard_approve_provider'),
    path('admin-dashboard/bookings/', admin_views.admin_manage_bookings, name='admin_manage_bookings'),
    path('admin-dashboard/bookings/<int:booking_id>/update/', admin_views.admin_update_booking_status, name='admin_dashboard_update_booking'),
    path('admin-dashboard/website/', admin_views.admin_manage_website, name='admin_manage_website'),
]
