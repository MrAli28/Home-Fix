// Main JavaScript for HomeFix

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