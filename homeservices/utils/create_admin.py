import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Check if user already exists
if not User.objects.filter(email='huss133236@gmail.com').exists():
    # Create superuser
    user = User.objects.create_superuser(
        username='admin',
        email='huss133236@gmail.com',
        password='MyNameisAli31'
    )
    print(f"Admin user created with email: {user.email}")
else:
    # Update existing user to be superuser
    user = User.objects.get(email='huss133236@gmail.com')
    user.is_staff = True
    user.is_superuser = True
    user.set_password('MyNameisAli31')
    user.save()
    print(f"Existing user updated to admin: {user.email}")