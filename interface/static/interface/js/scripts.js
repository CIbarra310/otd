// Function to hide About, Contact, and Services from the navbar when on the login or register page
function hideNavbarItemsOnAuthPages() {
    // Get the current path
    const path = window.location.pathname;
    
    // Check if the current path is 'login' or 'register'
    if (path.includes('login') || path.includes('register')) {
        // Hide the 'About', 'Contact', and 'Services' navigation items
        document.querySelector('.about').style.display = 'none';
        document.querySelector('.contact').style.display = 'none';
        document.querySelector('.services').style.display = 'none';
    }
}

// Other functions can be defined here
function anotherFunction() {
    // Code for another task
}

// Event listener for DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    hideNavbarItemsOnAuthPages();
    anotherFunction(); // Call other functions as needed
});


