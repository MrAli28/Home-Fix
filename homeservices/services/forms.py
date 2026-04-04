from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Provider, Review

class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BookingForm(forms.ModelForm):
    """Form for creating a service booking"""
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=255, required=True)
    postcode = forms.CharField(max_length=20, required=True)
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time', 'phone_number', 'email', 'address', 'postcode', 'notes']

class ProviderRegistrationForm(forms.ModelForm):
    """Form for registering as a service provider"""
    class Meta:
        model = Provider
        fields = ['service_types', 'experience', 'bio']
        widgets = {
            'experience': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

class ReviewForm(forms.ModelForm):
    """Form for submitting service reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
