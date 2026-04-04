// Main JavaScript for HomeFix

document.addEventListener('DOMContentLoaded', function() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add animation attributes automatically across pages.
    const animatedSelectors = [
        '.hero-section h1',
        '.hero-section p',
        '.hero-section .btn',
        '.services-header h1',
        '.services-header p',
        '.services-header .btn',
        '.card',
        '.service-card',
        '.testimonial-card',
        '.booking-card',
        '.list-group-item',
        '.alert',
        '.table-responsive',
        '.accordion-item',
        '.form-control',
        '.form-select',
        'section .row > [class*="col-"]'
    ];

    const uniqueEls = new Set();
    animatedSelectors.forEach(function(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            if (!el.closest('.modal')) {
                uniqueEls.add(el);
            }
        });
    });

    Array.from(uniqueEls).forEach(function(el, index) {
        if (!el.hasAttribute('data-animate')) {
            el.setAttribute('data-animate', index % 3 === 0 ? 'up' : index % 3 === 1 ? 'left' : 'right');
        }
        if (!el.style.getPropertyValue('--anim-delay')) {
            el.style.setProperty('--anim-delay', String((index % 8) * 45) + 'ms');
        }
    });

    document.querySelectorAll('.service-icon, .fa-star, .fa-award, .fa-shield-alt').forEach(function(icon) {
        if (!icon.hasAttribute('data-float')) {
            icon.setAttribute('data-float', 'true');
        }
    });

    if (!prefersReducedMotion) {
        const observer = new IntersectionObserver(function(entries, obs) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    obs.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -8% 0px'
        });

        document.querySelectorAll('[data-animate]').forEach(function(el) {
            observer.observe(el);
        });
    } else {
        document.querySelectorAll('[data-animate]').forEach(function(el) {
            el.classList.add('animate-in');
        });
    }

    // Soft magnetic hover for major action buttons.
    if (!prefersReducedMotion) {
        document.querySelectorAll('.btn-primary, .btn-outline-primary').forEach(function(btn) {
            btn.addEventListener('mousemove', function(event) {
                const rect = btn.getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;
                const moveX = (x / rect.width - 0.5) * 8;
                const moveY = (y / rect.height - 0.5) * 8;
                btn.style.transform = 'translate(' + moveX.toFixed(1) + 'px, ' + moveY.toFixed(1) + 'px)';
            });

            btn.addEventListener('mouseleave', function() {
                btn.style.transform = '';
            });
        });
    }
    
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
                    availabilityResult.innerHTML = '<div class="alert alert-warning">Sorry, we don't currently serve your area.</div>';
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
});