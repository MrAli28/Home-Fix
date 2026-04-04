import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import Service

# List of services to add with their descriptions and base prices
services_to_add = [
    {
        'name': 'Loft Conversions',
        'description': 'Transform your unused loft space into a functional living area. Our professional loft conversion services include design, structural work, insulation, electrical, plumbing, and finishing.',
        'icon': 'home',
        'base_price': 15000.00,
        'category': 'Building Works'
    },
    {
        'name': 'Extensions',
        'description': 'Expand your living space with our high-quality home extension services. We handle everything from planning and design to construction and finishing touches.',
        'icon': 'expand-arrows-alt',
        'base_price': 20000.00,
        'category': 'Building Works'
    },
    {
        'name': 'Painting',
        'description': 'Professional interior and exterior painting services to refresh and transform your space. We use high-quality paints and techniques for a flawless finish.',
        'icon': 'paint-roller',
        'base_price': 500.00,
        'category': 'Interior Finishing'
    },
    {
        'name': 'Wallpaper',
        'description': 'Expert wallpaper installation services to add style and character to your home. We offer a wide range of wallpaper options and professional installation.',
        'icon': 'scroll',
        'base_price': 400.00,
        'category': 'Interior Finishing'
    },
    {
        'name': 'Plastering',
        'description': 'High-quality plastering services for smooth, durable walls and ceilings. Our experienced plasterers can handle new builds, renovations, and repairs.',
        'icon': 'trowel',
        'base_price': 350.00,
        'category': 'Interior Finishing'
    },
    {
        'name': 'Bathroom Installation',
        'description': 'Complete bathroom installation and renovation services. From design to installation, we handle all aspects of creating your dream bathroom.',
        'icon': 'toilet',
        'base_price': 3500.00,
        'category': 'Plumbing'
    },
    {
        'name': 'Tiling Fittings',
        'description': 'Professional tiling services for bathrooms, kitchens, floors, and more. We offer expert installation of all types of tiles for a beautiful, long-lasting finish.',
        'icon': 'border-all',
        'base_price': 600.00,
        'category': 'Interior Finishing'
    },
    {
        'name': 'Electrical Work',
        'description': 'Comprehensive electrical services for residential and commercial properties. Our certified electricians can handle installations, repairs, and maintenance.',
        'icon': 'bolt',
        'base_price': 250.00,
        'category': 'Maintenance'
    },
    {
        'name': 'Plumbing',
        'description': 'Professional plumbing services including installations, repairs, and maintenance. Our experienced plumbers can handle all your plumbing needs.',
        'icon': 'faucet',
        'base_price': 200.00,
        'category': 'Maintenance'
    },
    {
        'name': 'House Renovation',
        'description': 'Complete house renovation services to transform your property. We handle everything from design and planning to construction and finishing.',
        'icon': 'home',
        'base_price': 25000.00,
        'category': 'Building Works'
    },
    {
        'name': 'Flooring',
        'description': 'Professional flooring installation services for all types of flooring materials. We offer expert installation of hardwood, laminate, vinyl, tile, and carpet.',
        'icon': 'th-large',
        'base_price': 1500.00,
        'category': 'Interior Finishing'
    },
]

def add_services():
    """Add services to the database if they don't already exist"""
    for service_data in services_to_add:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults={
                'description': service_data['description'],
                'icon': service_data['icon'],
                'base_price': service_data['base_price'],
                'category': service_data['category'],
            }
        )
        
        if created:
            print(f"Added service: {service.name}")
        else:
            print(f"Service already exists: {service.name}")

if __name__ == "__main__":
    print("Adding services to the database...")
    add_services()
    print("Done!")
