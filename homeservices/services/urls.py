from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    
    # Services
    path('services/', views.services_list, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Booking
    path('book/', views.book_service, name='book_service'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/rate/<int:booking_id>/', views.rate_booking, name='rate_booking'),
    path('bookings/update-status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    
    # User account
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='services/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='services/password_reset.html'), 
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
]
