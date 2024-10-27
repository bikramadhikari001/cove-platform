// Modern JavaScript for Covenant Tracking Platform

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initializeNavigation();
    initializeAnimations();
    initializeFormValidation();
    initializeLoadingStates();
    initializeTooltips();
    initializeCharts();
});

// Navigation Handling
function initializeNavigation() {
    // Add active state to current navigation item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Mobile navigation toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }
}

// Animations
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all animatable elements
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // Add hover animations to cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showFormErrors(this);
            }
        });

        // Real-time validation
        form.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('blur', function() {
                validateInput(this);
            });
        });
    });
}

function validateForm(form) {
    let isValid = true;
    form.querySelectorAll('input, select, textarea').forEach(input => {
        if (!validateInput(input)) {
            isValid = false;
        }
    });
    return isValid;
}

function validateInput(input) {
    const value = input.value.trim();
    let isValid = true;

    // Clear previous error messages
    const errorElement = input.nextElementSibling;
    if (errorElement && errorElement.classList.contains('error-message')) {
        errorElement.remove();
    }

    // Required field validation
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        showError(input, 'This field is required');
    }

    // Email validation
    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            showError(input, 'Please enter a valid email address');
        }
    }

    // Password validation
    if (input.type === 'password' && value) {
        if (value.length < 8) {
            isValid = false;
            showError(input, 'Password must be at least 8 characters long');
        }
    }

    // Update input styling
    input.classList.toggle('is-invalid', !isValid);
    input.classList.toggle('is-valid', isValid);

    return isValid;
}

function showError(input, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message text-danger mt-1';
    errorDiv.textContent = message;
    input.parentNode.insertBefore(errorDiv, input.nextSibling);
}

// Loading States
function initializeLoadingStates() {
    // Show loading state on form submit
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            }
        });
    });
}

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Charts and Data Visualization
function initializeCharts() {
    // Check if we're on a page that needs charts
    const chartElements = document.querySelectorAll('[data-chart]');
    if (chartElements.length > 0) {
        // Load Chart.js dynamically
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = function() {
            chartElements.forEach(createChart);
        };
        document.head.appendChild(script);
    }
}

function createChart(element) {
    const type = element.dataset.chart;
    const ctx = element.getContext('2d');
    
    // Example chart data
    const data = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [{
            label: 'Covenant Compliance',
            data: [98, 95, 97, 96, 98, 99],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            tension: 0.4
        }]
    };

    const config = {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    };

    new Chart(ctx, config);
}

// Flash Messages
function showFlashMessage(message, type = 'info') {
    const flashContainer = document.createElement('div');
    flashContainer.className = `alert alert-${type} alert-dismissible fade show`;
    flashContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('main').insertAdjacentElement('afterbegin', flashContainer);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        flashContainer.classList.remove('show');
        setTimeout(() => flashContainer.remove(), 300);
    }, 5000);
}

// API Request Helper
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    };

    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showFlashMessage('An error occurred while processing your request.', 'danger');
        throw error;
    }
}

// Dark Mode Toggle
function initializeDarkMode() {
    const darkModeToggle = document.querySelector('#darkModeToggle');
    if (darkModeToggle) {
        // Check user preference
        if (localStorage.getItem('darkMode') === 'enabled' || 
            (window.matchMedia('(prefers-color-scheme: dark)').matches && 
             !localStorage.getItem('darkMode'))) {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }

        darkModeToggle.addEventListener('change', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', 
                document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled'
            );
        });
    }
}

// Initialize dark mode
initializeDarkMode();
