// Hide About, Contact, and Services from the navbar when on the login or register page
    document.addEventListener('DOMContentLoaded', () => {
        // Get the current path
        const path = window.location.pathname;
        
        // Check if the current path is 'login.html'
        if (path.includes('login.html') || path.includes('register.html')) {
            // Hide the 'About', 'Contact', and 'Services' navigation items
            document.querySelector('.nav-item.about').style.display = 'none';
            document.querySelector('.nav-item.contact').style.display = 'none';
            document.querySelector('.nav-item.services').style.display = 'none';
        }
    });

