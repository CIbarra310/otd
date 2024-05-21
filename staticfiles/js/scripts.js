// Hide About, Contact, and Services from the navbar when on the login or register page
document.addEventListener('DOMContentLoaded', () => {
    // Get the current path
    const path = window.location.pathname;
    
    // Check if the current path is 'login.html' or 'register.html'
    if (path.includes('login.html') || path.includes('register.html')) {
        // Hide the 'About', 'Contact', and 'Services' navigation items
        document.querySelector('.about').style.display = 'none';
        document.querySelector('.contact').style.display = 'none';
        document.querySelector('.services').style.display = 'none';
    }
});

