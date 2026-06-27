"""
HomeFix Master Seed Script
===========================
Runs automatically on every startup via start.sh
Creates all required data if it doesn't already exist.
- Admin user
- Services
- Service Areas
- Providers (approved, with known credentials)
- Test Customer
"""

import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from services.models import Service, Provider, ServiceArea


def seed_admin():
    """Create admin superuser if not exists."""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@homefix.com',
            password='KazimAli31',
            first_name='Admin',
            last_name='HomeFix'
        )
        print("  [+] Admin created  -> username: admin | password: KazimAli31")
    else:
        # Make sure password is always correct even if someone changed it
        u = User.objects.get(username='admin')
        u.set_password('KazimAli31')
        u.is_staff = True
        u.is_superuser = True
        u.email = 'admin@homefix.com'
        u.save()
        print("  [=] Admin already exists — password reset to KazimAli31")


def seed_test_customer():
    """Create a test customer account if not exists."""
    if not User.objects.filter(username='customer1').exists():
        User.objects.create_user(
            username='customer1',
            email='customer@homefix.com',
            password='Customer123!',
            first_name='Ali',
            last_name='Kazim'
        )
        print("  [+] Test Customer  -> username: customer1 | password: Customer123!")
    else:
        print("  [=] Test Customer already exists")


def seed_services():
    """Create services if not exist."""
    services_data = [
        ("Plumbing",    "Expert plumbing services for all your needs",     "fa-wrench",         60.00, "Maintenance"),
        ("Electrical",  "Certified electrical repairs and installations",  "fa-bolt",           75.00, "Maintenance"),
        ("Cleaning",    "Professional house & office cleaning",            "fa-broom",          45.00, "Cleaning"),
        ("Gardening",   "Lawn care, landscaping and garden maintenance",   "fa-leaf",           50.00, "Outdoors"),
        ("Painting",    "Interior and exterior painting services",         "fa-paint-roller",   55.00, "Improvement"),
        ("Carpentry",   "Custom woodwork, furniture and repairs",          "fa-hammer",         65.00, "Improvement"),
    ]
    created = 0
    for name, desc, icon, price, cat in services_data:
        _, was_created = Service.objects.get_or_create(
            name=name,
            defaults=dict(description=desc, icon=icon, base_price=price, category=cat)
        )
        if was_created:
            created += 1
    print(f"  [+] Services: {created} new created, {len(services_data)-created} already existed")


def seed_areas():
    """Create service areas if not exist."""
    areas_data = [
        ("London",     "E1, E2, N1, NW1, W1, WC1, SW1, SE1, EC1"),
        ("Manchester", "M1, M2, M3, M4, M14, M15, M16"),
        ("Birmingham", "B1, B2, B3, B4, B5, B11, B12"),
    ]
    created = 0
    for city, postcodes in areas_data:
        _, was_created = ServiceArea.objects.get_or_create(
            city=city,
            defaults=dict(postcodes=postcodes)
        )
        if was_created:
            created += 1
    print(f"  [+] Service Areas: {created} new created, {len(areas_data)-created} already existed")


def seed_providers():
    """Create approved providers for each service/area combo if not exist."""
    first_names = ["John", "Sarah", "Mike", "Emma", "David", "Lucy",
                   "James", "Lisa", "Tom", "Anna", "Robert", "Emily",
                   "William", "Olivia", "Charlie", "Sophia"]
    last_names  = ["Smith", "Jones", "Brown", "Davis", "Wilson", "Taylor",
                   "Evans", "Thomas", "Roberts", "Walker", "Wright",
                   "Robinson", "Thompson", "Hughes", "Edwards", "Green"]

    areas    = list(ServiceArea.objects.all())
    services = list(Service.objects.all())

    if not areas or not services:
        print("  [!] No areas/services found — skipping providers")
        return

    created = 0
    ratings   = [5.0, 4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2]
    job_counts = [150, 130, 120, 95, 85, 70, 60, 45, 30]

    for area in areas:
        for svc in services:
            for i in range(9):
                username = f"provider_{area.city.lower()}_{svc.name.lower()}_{i}"

                if User.objects.filter(username=username).exists():
                    # Make sure provider is approved
                    try:
                        p = Provider.objects.get(user__username=username)
                        if not p.is_approved:
                            p.is_approved = True
                            p.save()
                    except Provider.DoesNotExist:
                        pass
                    continue

                fn = random.choice(first_names)
                ln = random.choice(last_names)

                user = User.objects.create_user(
                    username=username,
                    password='HomefixPro123!',
                    first_name=fn,
                    last_name=ln
                )

                provider = Provider.objects.create(
                    user=user,
                    phone=f"+44 7{random.randint(100,999)} {random.randint(100,999)} {random.randint(1000,9999)}",
                    experience=f"{random.randint(3, 15)} years",
                    bio=f"Expert {svc.name.lower()} professional providing top-notch services in {area.city}.",
                    rating=ratings[i],
                    total_jobs=job_counts[i],
                    is_approved=True
                )
                provider.service_types.set([svc])
                provider.service_areas.set([area])
                created += 1

    print(f"  [+] Providers: {created} new created")
    if created == 0:
        print("  [=] All providers already exist and are approved")


def run():
    print("\n======================================")
    print("  HomeFix — Database Seed Starting")
    print("======================================")

    print("\n[1/4] Admin Account")
    seed_admin()

    print("\n[2/4] Test Customer")
    seed_test_customer()

    print("\n[3/4] Services & Areas")
    seed_services()
    seed_areas()

    print("\n[4/4] Providers")
    seed_providers()

    print("\n======================================")
    print("  Seed Complete! Ready to go.")
    print("--------------------------------------")
    print("  ADMIN     -> admin / KazimAli31")
    print("  CUSTOMER  -> customer1 / Customer123!")
    print("  PROVIDERS -> provider_london_plumbing_0 / HomefixPro123!")
    print("======================================\n")


if __name__ == '__main__':
    run()
