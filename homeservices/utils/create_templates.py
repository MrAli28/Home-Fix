import os
import sys

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def create_file(path, content):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Created file: {path}")

def main():
    # Create template directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    services_templates_dir = os.path.join(templates_dir, 'services')
    
    create_directory(templates_dir)
    create_directory(services_templates_dir)
    
    # Create static directories
    static_dir = os.path.join(base_dir, 'static')
    css_dir = os.path.join(static_dir, 'css')
    js_dir = os.path.join(static_dir, 'js')
    
    create_directory(static_dir)
    create_directory(css_dir)
    create_directory(js_dir)
    
    # Create base.html
    base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}HomeFix - Professional Home Services{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="/static/css/styles.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">
                <i class="fas fa-tools me-2"></i>HomeFix
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'services' %}">Services</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'providers' %}">Providers</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'about' %}">About Us</a>
                    </li>
                </ul>
                <div class="navbar-nav">
                    {% if user.is_authenticated %}
                        <div class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user-circle me-1"></i>{{ user.first_name|default:user.username }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="{% url 'dashboard' %}">Dashboard</a></li>
                                <li><a class="dropdown-item" href="{% url 'profile' %}">Profile</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{% url 'logout' %}">Logout</a></li>
                            </ul>
                        </div>
                    {% else %}
                        <a class="nav-link" href="{% url 'login' %}">Login</a>
                        <a class="nav-link btn btn-outline-light ms-2" href="{% url 'register' %}">Sign Up</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>

    <!-- Messages/Alerts -->
    {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Main Content -->
    <main class="py-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <h5>HomeFix</h5>
                    <p>Your trusted partner for professional home services.</p>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="{% url 'home' %}" class="text-white">Home</a></li>
                        <li><a href="{% url 'services' %}" class="text-white">Services</a></li>
                        <li><a href="{% url 'about' %}" class="text-white">About Us</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Contact Us</h5>
                    <address>
                        <i class="fas fa-map-marker-alt me-2"></i>123 Service St, London, UK<br>
                        <i class="fas fa-phone me-2"></i>(123) 456-7890<br>
                        <i class="fas fa-envelope me-2"></i>info@homefix.com
                    </address>
                </div>
            </div>
            <hr>
            <div class="text-center">
                <p class="mb-0">&copy; {% now "Y" %} HomeFix. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Custom JS -->
    <script src="/static/js/main.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>"""
    
    # Create home.html
    home_html = """{% extends "base.html" %}

{% block title %}HomeFix - Professional Home Services{% endblock %}

{% block content %}
<div class="container">
    <!-- Hero Section -->
    <section class="py-5 text-center">
        <div class="row py-lg-5">
            <div class="col-lg-8 col-md-10 mx-auto">
                <h1 class="fw-bold">Professional Home Services</h1>
                <p class="lead text-muted">
                    Find trusted professionals for all your home service needs.
                    From plumbing and electrical work to cleaning and gardening.
                </p>
                <div class="d-flex justify-content-center gap-2">
                    <a href="{% url 'services' %}" class="btn btn-primary btn-lg px-4">Browse Services</a>
                    <a href="{% url 'providers' %}" class="btn btn-outline-secondary btn-lg px-4">Find Providers</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Search Section -->
    <section class="py-4 bg-light rounded">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <h2 class="text-center mb-4">Find a Service</h2>
                    <form action="{% url 'services' %}" method="get" class="row g-3">
                        <div class="col-md-5">
                            <select name="service" class="form-select form-select-lg">
                                <option value="">Select a service</option>
                                {% for service in services %}
                                <option value="{{ service.id }}">{{ service.name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-5">
                            <input type="text" name="postcode" class="form-control form-control-lg" placeholder="Enter your postcode">
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-primary btn-lg w-100">Search</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section class="py-5">
        <h2 class="text-center mb-4">Our Services</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
            {% for service in services %}
            <div class="col">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <div class="text-center mb-3">
                            <i class="fas fa-{{ service.icon }} fa-3x text-primary"></i>
                        </div>
                        <h5 class="card-title text-center">{{ service.name }}</h5>
                        <p class="card-text">{{ service.description }}</p>
                        <p class="text-center text-muted">Starting from £{{ service.base_price }}</p>
                    </div>
                    <div class="card-footer bg-transparent border-0 text-center">
                        <a href="{% url 'service_detail' service.id %}" class="btn btn-outline-primary">Learn More</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- How It Works Section -->
    <section class="py-5 bg-light rounded">
        <h2 class="text-center mb-5">How It Works</h2>
        <div class="row g-4">
            <div class="col-md-4 text-center">
                <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-3" style="width: 80px; height: 80px;">
                    <i class="fas fa-search fa-2x"></i>
                </div>
                <h4>1. Find a Service</h4>
                <p>Browse our range of professional home services or search for a specific service you need.</p>
            </div>
            <div class="col-md-4 text-center">
                <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-3" style="width: 80px; height: 80px;">
                    <i class="fas fa-calendar-alt fa-2x"></i>
                </div>
                <h4>2. Book an Appointment</h4>
                <p>Choose a convenient date and time for your service appointment.</p>
            </div>
            <div class="col-md-4 text-center">
                <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-3" style="width: 80px; height: 80px;">
                    <i class="fas fa-check-circle fa-2x"></i>
                </div>
                <h4>3. Get the Job Done</h4>
                <p>Our professional service provider will arrive and complete the job to your satisfaction.</p>
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-5">
        <h2 class="text-center mb-4">What Our Customers Say</h2>
        <div class="row">
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-center mb-3">
                            <div class="text-warning">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                            </div>
                        </div>
                        <p class="card-text">"Excellent service! The plumber arrived on time and fixed our leaking pipe quickly. Very professional and friendly."</p>
                        <div class="text-end">
                            <p class="mb-0 fw-bold">- Sarah Johnson</p>
                            <small class="text-muted">London</small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-center mb-3">
                            <div class="text-warning">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                            </div>
                        </div>
                        <p class="card-text">"I've used HomeFix for electrical work and gardening. Both times the service was outstanding. Will definitely use again!"</p>
                        <div class="text-end">
                            <p class="mb-0 fw-bold">- Michael Brown</p>
                            <small class="text-muted">Manchester</small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-center mb-3">
                            <div class="text-warning">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="far fa-star"></i>
                            </div>
                        </div>
                        <p class="card-text">"The cleaning service was thorough and efficient. My house hasn't been this clean in ages! Booking was easy and straightforward."</p>
                        <div class="text-end">
                            <p class="mb-0 fw-bold">- Emma Wilson</p>
                            <small class="text-muted">Birmingham</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>
{% endblock %}"""
    
    # Create dashboard.html
    dashboard_html = """{% extends "base.html" %}

{% block title %}Dashboard - HomeFix{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-lg-3 mb-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dashboard</h5>
                </div>
                <div class="list-group list-group-flush">
                    <a href="#bookings" class="list-group-item list-group-item-action active" data-bs-toggle="list">
                        <i class="fas fa-calendar-alt me-2"></i>My Bookings
                    </a>
                    <a href="#profile" class="list-group-item list-group-item-action" data-bs-toggle="list">
                        <i class="fas fa-user me-2"></i>Profile
                    </a>
                    <a href="#settings" class="list-group-item list-group-item-action" data-bs-toggle="list">
                        <i class="fas fa-cog me-2"></i>Settings
                    </a>
                </div>
                <div class="card-footer">
                    <a href="{% url 'book' %}" class="btn btn-primary w-100">
                        <i class="fas fa-plus me-2"></i>New Booking
                    </a>
                </div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="col-lg-9">
            <div class="tab-content">
                <!-- Bookings Tab -->
                <div class="tab-pane fade show active" id="bookings">
                    <div class="card">
                        <div class="card-header">
                            <ul class="nav nav-tabs card-header-tabs" id="bookingTabs" role="tablist">
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link active" id="upcoming-tab" data-bs-toggle="tab" data-bs-target="#upcoming" type="button" role="tab">
                                        Upcoming Bookings
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="past-tab" data-bs-toggle="tab" data-bs-target="#past" type="button" role="tab">
                                        Past Bookings
                                    </button>
                                </li>
                            </ul>
                        </div>
                        <div class="card-body">
                            <div class="tab-content" id="bookingTabsContent">
                                <!-- Upcoming Bookings -->
                                <div class="tab-pane fade show active" id="upcoming" role="tabpanel">
                                    {% if upcoming_bookings %}
                                        {% for booking in upcoming_bookings %}
                                        <div class="card mb-3">
                                            <div class="card-body">
                                                <div class="row">
                                                    <div class="col-md-8">
                                                        <h5 class="card-title">{{ booking.service.name }}</h5>
                                                        <p class="card-text">
                                                            <strong>Date:</strong> {{ booking.date|date:"F j, Y" }}<br>
                                                            <strong>Time:</strong> {{ booking.time|time:"g:i A" }}<br>
                                                            <strong>Address:</strong> {{ booking.address }}, {{ booking.postcode }}<br>
                                                            <strong>Status:</strong> 
                                                            <span class="badge {% if booking.status == 'confirmed' %}bg-success{% else %}bg-warning{% endif %}">
                                                                {{ booking.status|title }}
                                                            </span>
                                                        </p>
                                                        {% if booking.notes %}
                                                        <p class="card-text"><strong>Notes:</strong> {{ booking.notes }}</p>
                                                        {% endif %}
                                                    </div>
                                                    <div class="col-md-4 text-md-end">
                                                        <p class="card-text">
                                                            <strong>Price:</strong> £{{ booking.price|default:"TBD" }}
                                                        </p>
                                                        <a href="{% url 'cancel_booking' booking.id %}" class="btn btn-outline-danger">
                                                            <i class="fas fa-times me-1"></i>Cancel
                                                        </a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        {% endfor %}
                                    {% else %}
                                        <div class="text-center py-4">
                                            <i class="fas fa-calendar-alt fa-3x text-muted mb-3"></i>
                                            <p class="lead">You don't have any upcoming bookings.</p>
                                            <a href="{% url 'services' %}" class="btn btn-primary">Browse Services</a>
                                        </div>
                                    {% endif %}
                                </div>
                                
                                <!-- Past Bookings -->
                                <div class="tab-pane fade" id="past" role="tabpanel">
                                    {% if past_bookings %}
                                        {% for booking in past_bookings %}
                                        <div class="card mb-3">
                                            <div class="card-body">
                                                <div class="row">
                                                    <div class="col-md-8">
                                                        <h5 class="card-title">{{ booking.service.name }}</h5>
                                                        <p class="card-text">
                                                            <strong>Date:</strong> {{ booking.date|date:"F j, Y" }}<br>
                                                            <strong>Time:</strong> {{ booking.time|time:"g:i A" }}<br>
                                                            <strong>Address:</strong> {{ booking.address }}, {{ booking.postcode }}<br>
                                                            <strong>Status:</strong> 
                                                            <span class="badge {% if booking.status == 'completed' %}bg-success{% else %}bg-danger{% endif %}">
                                                                {{ booking.status|title }}
                                                            </span>
                                                        </p>
                                                    </div>
                                                    <div class="col-md-4 text-md-end">
                                                        <p class="card-text">
                                                            <strong>Price:</strong> £{{ booking.price }}
                                                        </p>
                                                        {% if booking.status == 'completed' and not booking.rating %}
                                                        <a href="{% url 'rate_booking' booking.id %}" class="btn btn-outline-primary">
                                                            <i class="fas fa-star me-1"></i>Leave Review
                                                        </a>
                                                        {% elif booking.rating %}
                                                        <div class="text-warning">
                                                            {% for i in "12345"|make_list %}
                                                                {% if forloop.counter <= booking.rating %}
                                                                <i class="fas fa-star"></i>
                                                                {% else %}
                                                                <i class="far fa-star"></i>
                                                                {% endif %}
                                                            {% endfor %}
                                                        </div>
                                                        {% endif %}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        {% endfor %}
                                    {% else %}
                                        <div class="text-center py-4">
                                            <i class="fas fa-history fa-3x text-muted mb-3"></i>
                                            <p class="lead">You don't have any past bookings.</p>
                                        </div>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Profile Tab -->
                <div class="tab-pane fade" id="profile">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Personal Information</h5>
                        </div>
                        <div class="card-body">
                            <form method="post" action="{% url 'profile' %}">
                                {% csrf_token %}
                                <div class="row mb-3">
                                    <div class="col-md-6">
                                        <label for="first_name" class="form-label">First Name</label>
                                        <input type="text" class="form-control" id="first_name" name="first_name" value="{{ user.first_name }}">
                                    </div>
                                    <div class="col-md-6">
                                        <label for="last_name" class="form-label">Last Name</label>
                                        <input type="text" class="form-control" id="last_name" name="last_name" value="{{ user.last_name }}">
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="email" class="form-label">Email Address</label>
                                    <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}">
                                </div>
                                <button type="submit" class="btn btn-primary">Update Profile</button>
                            </form>
                        </div>
                    </div>
                    
                    <div class="card mt-4">
                        <div class="card-header">
                            <h5 class="mb-0">Become a Service Provider</h5>
                        </div>
                        <div class="card-body">
                            <p>Would you like to offer your services on HomeFix?</p>
                            <a href="{% url 'become_provider' %}" class="btn btn-outline-primary">Apply Now</a>
                        </div>
                    </div>
                </div>
                
                <!-- Settings Tab -->
                <div class="tab-pane fade" id="settings">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Account Settings</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-4">
                                <h6>Password</h6>
                                <p class="text-muted">Change your account password</p>
                                <a href="{% url 'password_reset' %}" class="btn btn-outline-primary">Change Password</a>
                            </div>
                            <hr>
                            <div class="mb-4">
                                <h6>Notifications</h6>
                                <p class="text-muted">Manage your notification preferences</p>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="emailNotifications" checked>
                                    <label class="form-check-label" for="emailNotifications">Email Notifications</label>
                                </div>
                                <div class="form-check form-switch mt-2">
                                    <input class="form-check-input" type="checkbox" id="smsNotifications">
                                    <label class="form-check-label" for="smsNotifications">SMS Notifications</label>
                                </div>
                            </div>
                            <hr>
                            <div>
                                <h6>Delete Account</h6>
                                <p class="text-muted">Permanently delete your account and all data</p>
                                <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteAccountModal">
                                    Delete Account
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Delete Account Modal -->
<div class="modal fade" id="deleteAccountModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Confirm Account Deletion</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete your account? This action cannot be undone and all your data will be permanently removed.</p>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="confirmDelete">
                    <label class="form-check-label" for="confirmDelete">
                        I understand that this action is permanent
                    </label>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" id="deleteAccountBtn" disabled>Delete Account</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Enable/disable delete account button based on checkbox
    document.addEventListener('DOMContentLoaded', function() {
        const confirmDeleteCheckbox = document.getElementById('confirmDelete');
        const deleteAccountBtn = document.getElementById('deleteAccountBtn');
        
        if (confirmDeleteCheckbox && deleteAccountBtn) {
            confirmDeleteCheckbox.addEventListener('change', function() {
                deleteAccountBtn.disabled = !this.checked;
            });
        }
        
        // Handle tab navigation from URL hash
        const hash = window.location.hash;
        if (hash) {
            const triggerEl = document.querySelector(`.list-group-item[href="${hash}"]`);
            if (triggerEl) {
                const tab = new bootstrap.Tab(triggerEl);
                tab.show();
            }
        }
    });
</script>
{% endblock %}"""

    # Create CSS file
    css_content = """/* Custom styles for HomeFix */

/* General styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
}

/* Hero section */
.hero-section {
    background-color: #f8f9fa;
    padding: 5rem 0;
}

/* Service cards */
.service-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.service-icon {
    font-size: 3rem;
    color: #0d6efd;
    margin-bottom: 1rem;
}

/* Testimonials */
.testimonial-card {
    border-radius: 10px;
    overflow: hidden;
}

/* Dashboard */
.dashboard-sidebar {
    position: sticky;
    top: 2rem;
}

/* Booking cards */
.booking-card {
    border-left: 5px solid #0d6efd;
}

.booking-card.completed {
    border-left-color: #198754;
}

    border-left-color: #dc3545;
}

/* Forms */
.form-control:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Buttons */
.btn-primary {
    background-color: #0d6efd;
    border-color: #0d6efd;
}

.btn-primary:hover {
    background-color: #0b5ed7;
    border-color: #0a58ca;
}

/* Footer */
footer a {
    text-decoration: none;
}

footer a:hover {
    text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .hero-section {
        padding: 3rem 0;
    }
}"""

    # Create JavaScript file
    js_content = """// Main JavaScript for HomeFix

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Postcode availability check
    const postcodeForm = document.getElementById('postcodeCheckForm');
    if (postcodeForm) {
        postcodeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const postcode = document.getElementById('postcode').value.trim();
            if (!postcode) return;
            
            // AJAX request would go here in a real app
            // For demo, we'll simulate a response
            const availabilityResult = document.getElementById('availabilityResult');
            
            // Simulate API call delay
            availabilityResult.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
            
            setTimeout(function() {
                // Simulate a positive response for demo purposes
                if (postcode.toUpperCase().startsWith('E') || postcode.toUpperCase().startsWith('SW') || postcode.toUpperCase().startsWith('W')) {
                    availabilityResult.innerHTML = '<div class="alert alert-success">Great news! We serve your area.</div>';
                } else {
                    availabilityResult.innerHTML = '<div class="alert alert-warning">Sorry, we don\'t currently serve your area.</div>';
                }
            }, 1000);
        });
    }
    
    // Booking form date validation
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        const dateInput = document.getElementById('date');
        if (dateInput) {
            // Set minimum date to today
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            dateInput.min = `${yyyy}-${mm}-${dd}`;
            
            // Validate date is not in the past
            bookingForm.addEventListener('submit', function(e) {
                const selectedDate = new Date(dateInput.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                if (selectedDate < today) {
                    e.preventDefault();
                    alert('Please select a future date for your booking.');
                }
            });
        }
    }
});"""

    # Create the files
    create_file(os.path.join(templates_dir, 'base.html'), base_html)
    create_file(os.path.join(services_templates_dir, 'home.html'), home_html)
    create_file(os.path.join(services_templates_dir, 'dashboard.html'), dashboard_html)
    create_file(os.path.join(css_dir, 'styles.css'), css_content)
    create_file(os.path.join(js_dir, 'main.js'), js_content)
    
    print("\nTemplate files created successfully!")
    print("To complete the setup, run the following commands:")
    print("1. pip install -r requirements.txt")
    print("2. python manage.py makemigrations")
    print("3. python manage.py migrate")
    print("4. python manage.py createsuperuser")
    print("5. python manage.py runserver")

if __name__ == "__main__":
    main()