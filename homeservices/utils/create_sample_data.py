import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from services.models import Service, ServiceArea, Provider

def create_sample_data():
    print("Creating sample data...")
    
    # Create services
    services_data = [
        {
            'name': 'Plumbing',
            'description': 'Repairs, installations, and maintenance for all plumbing systems',
            'icon': 'droplet',
            'base_price': 85,
            'category': 'Repairs',
        },
        {
            'name': 'Electrical',
            'description': 'Electrical repairs, installations, and inspections',
            'icon': 'zap',
            'base_price': 95,
            'category': 'Repairs',
        },
        {
            'name': 'Painting',
            'description': 'Interior and exterior painting services',
            'icon': 'brush',
            'base_price': 200,
            'category': 'Home Improvement',
        },
        {
            'name': 'Cleaning',
            'description': 'Professional cleaning services for homes and offices',
            'icon': 'sparkles',
            'base_price': 70,
            'category': 'Maintenance',
        },
        {
            'name': 'Gardening',
            'description': 'Lawn care, landscaping, and garden maintenance',
            'icon': 'flower',
            'base_price': 65,
            'category': 'Outdoors',
        },
        {
            'name': 'Carpentry',
            'description': 'Custom woodwork, repairs, and furniture assembly',
            'icon': 'hammer',
            'base_price': 110,
            'category': 'Home Improvement',
        },
    ]
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f"Created service: {service.name}")
        else:
            print(f"Service already exists: {service.name}")
    
    # Create service areas
    areas_data = [
        {
            'city': 'London',
            'postcodes': 'E1, EC1, W1, SW1, NW1, SE1, N1',
        },
        {
            'city': 'Manchester',
            'postcodes': 'M1, M2, M3, M4, M5',
        },
        {
            'city': 'Birmingham',
            'postcodes': 'B1, B2, B3, B4, B5',
        },
    ]
    
    for area_data in areas_data:
        area, created = ServiceArea.objects.get_or_create(
            city=area_data['city'],
            defaults=area_data
        )
        if created:
            print(f"Created service area: {area.city}")
        else:
            print(f"Service area already exists: {area.city}")
    
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        print("Created admin user (username: admin, password: adminpassword)")
    else:
        print("Admin user already exists")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()
