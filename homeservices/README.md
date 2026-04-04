# HomeFix - Home Services Platform

This is a Django-based web application for home services booking and management. It was converted from a React/TypeScript project to a Django project with HTML, CSS, and JavaScript.

## Features

- User authentication and registration
- Service browsing and filtering
- Service provider profiles
- Booking management
- Reviews and ratings
- User dashboard
- Responsive design

## Project Structure

```
home_services/
├── manage.py
├── config/  # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── services/  # Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/  # HTML templates
│   ├── base.html
│   └── services/
│       ├── home.html
│       ├── dashboard.html
│       └── ...
└── static/  # Static files
    ├── css/
    ├── js/
    └── images/
```

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Conversion Notes

This project was converted from a React/TypeScript application with Tailwind CSS to a Django application with Bootstrap and vanilla JavaScript. The conversion maintained the same functionality and UI design while adapting to Django's template-based architecture.

### Key Changes

- React components → Django templates
- TypeScript → Python and JavaScript
- Tailwind CSS → Bootstrap 5
- React Router → Django URL patterns
- Zustand state management → Django session management
- Mock API → Django models and views

## License

MIT
