import os
import django
import random
from django.apps import apps

if not apps.ready:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from django.contrib.auth.models import User
from services.models import Service, Provider, ServiceArea

def run():
    print("Clearing old providers (keeping services and areas)...")
    Provider.objects.all().delete()
    User.objects.filter(username__startswith='provider_').delete()
    
    # Check if areas and services exist, if not create them.
    if ServiceArea.objects.count() == 0:
        ServiceArea.objects.create(city="London", postcodes="E1, E2, N1, NW1, W1, WC1, SW1")
        ServiceArea.objects.create(city="Manchester", postcodes="M1, M2, M3, M4")
        ServiceArea.objects.create(city="Birmingham", postcodes="B1, B2, B3, B4")
        
    areas = list(ServiceArea.objects.all())
    
    if Service.objects.count() == 0:
        services_data = [
            ("Plumbing", "Expert plumbing services", "water", 60.00, "Maintenance"),
            ("Electrical", "Certified electrical repairs", "bolt", 75.00, "Maintenance"),
            ("Cleaning", "Professional house cleaning", "broom", 45.00, "Cleaning"),
            ("Gardening", "Lawn care and landscaping", "leaf", 50.00, "Outdoors"),
            ("Painting", "Interior and exterior painting", "paint-roller", 55.00, "Improvement"),
            ("Carpentry", "Custom woodwork and repairs", "hammer", 65.00, "Improvement"),
        ]
        for name, desc, icon, price, cat in services_data:
            Service.objects.create(name=name, description=desc, icon=icon, base_price=price, category=cat)

    services = list(Service.objects.all())
    
    print("Creating 3 Providers for EACH Service in EACH Area...")
    first_names = ["John", "Sarah", "Mike", "Emma", "David", "Lucy", "James", "Lisa", "Tom", "Anna", "Robert", "Emily", "William", "Olivia", "Charlie", "Sophia", "Thomas", "Isabella"]
    last_names = ["Smith", "Jones", "Brown", "Davis", "Wilson", "Taylor", "Evans", "Thomas", "Roberts", "Walker", "Wright", "Robinson", "Thompson", "White", "Hughes", "Edwards", "Green", "Hall"]
    
    provider_count = 0
    for area in areas:
        for s in services:
            # Create 3 providers for this service in this area
            for i in range(3):
                fn = random.choice(first_names)
                ln = random.choice(last_names)
                
                # Rank them cleanly, e.g. 5.0, 4.8, 4.5
                ratings = [5.0, 4.8, 4.5]
                jobs_count = [120, 85, 45]
                
                user = User.objects.create_user(
                    username=f"provider_{area.city.lower()}_{s.name.lower()}_{i}", 
                    password="password123", 
                    first_name=fn, 
                    last_name=ln
                )
                
                provider = Provider.objects.create(
                    user=user,
                    experience=f"{random.randint(3, 15)} years",
                    bio=f"Expert {s.name.lower()} professional providing top-notch services exclusively in {area.city}.",
                    rating=ratings[i],
                    total_jobs=jobs_count[i]
                )
                
                # Link to THIS service
                provider.service_types.set([s])
                
                # Link to THIS area ONLY
                provider.service_areas.set([area])
                
                provider_count += 1

    print(f"Done seeding {provider_count} providers!")

if __name__ == '__main__':
    run()
