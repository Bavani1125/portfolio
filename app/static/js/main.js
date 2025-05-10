// Main JavaScript file for the portfolio application

// DOM Elements
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');
const themeToggle = document.querySelector('.theme-toggle');
const closeAlertBtns = document.querySelectorAll('.close-alert');

// Toggle mobile menu
if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        
        // Toggle hamburger to X animation
        const spans = mobileMenuBtn.querySelectorAll('span');
        spans[0].classList.toggle('rotated');
        spans[1].classList.toggle('hidden');
        spans[2].classList.toggle('rotated-reverse');
    });
}

// Theme toggle functionality
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark-mode');
        
        // Save theme preference
        if (document.documentElement.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });
}

// Close alerts
if (closeAlertBtns.length > 0) {
    closeAlertBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const alert = btn.parentElement;
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        });
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            
            // Close mobile menu if open
            if (navLinks && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
            }
        }
    });
});

// Add CSS class for navbar when scrolling
const navbar = document.querySelector('.navbar');
if (navbar) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Animate elements when they come into view
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.timeline-item, .education-card, .skill-category, .project-card, .certification-card');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.2;
        
        if (elementPosition < screenPosition) {
            element.classList.add('animate-in');
        }
    });
};

// Add animation CSS class
document.addEventListener('DOMContentLoaded', () => {
    // Add animation CSS classes
    const style = document.createElement('style');
    style.textContent = `
        .timeline-item, .education-card, .skill-category, .project-card, .certification-card {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        .navbar.scrolled {
            background-color: rgba(var(--primary-color-rgb), 0.95);
            box-shadow: var(--shadow-md);
        }
        
        .mobile-menu-btn span.rotated {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .mobile-menu-btn span.hidden {
            opacity: 0;
        }
        
        .mobile-menu-btn span.rotated-reverse {
            transform: rotate(-45deg) translate(5px, -5px);
        }
    `;
    document.head.appendChild(style);
    
    // Initialize animation
    animateOnScroll();
    
    // Listen for scroll events
    window.addEventListener('scroll', animateOnScroll);
});

// Form Validation
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Get form fields
        const nameInput = this.querySelector('input[name="name"]');
        const emailInput = this.querySelector('input[name="email"]');
        const messageInput = this.querySelector('textarea[name="message"]');
        
        // Clear previous error messages
        document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
        
        // Validate name
        if (!nameInput.value.trim()) {
            isValid = false;
            showError(nameInput, 'Please enter your name');
        }
        
        // Validate email
        if (!emailInput.value.trim()) {
            isValid = false;
            showError(emailInput, 'Please enter your email');
        } else if (!isValidEmail(emailInput.value)) {
            isValid = false;
            showError(emailInput, 'Please enter a valid email address');
        }
        
        // Validate message
        if (!messageInput.value.trim()) {
            isValid = false;
            showError(messageInput, 'Please enter your message');
        } else if (messageInput.value.trim().length < 10) {
            isValid = false;
            showError(messageInput, 'Message must be at least 10 characters long');
        }
        
        // Prevent form submission if invalid
        if (!isValid) {
            e.preventDefault();
        }
    });
}

// Helper function to display error messages
function showError(input, message) {
    const formGroup = input.parentElement;
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.innerText = message;
    formGroup.appendChild(errorDiv);
    input.classList.add('is-invalid');
}

// Helper function to validate email
function isValidEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}