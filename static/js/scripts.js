console.log('Document loaded'); // Check if this prints

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired'); // Check if this prints

    // Get the current path
    const path = window.location.pathname;
    console.log('Current path:', path); // Check if this prints

    // Check if the current path is not 'index.html', 'login.html', or 'register' (or their equivalents)
    if (!(path === "/index.html" || path === "/login.html" || path === "/index" || path === "/login" || path === "/register")) {
        console.log('Path does not match index.html, login.html, or register');

        // Show the sidebar on all other pages
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.display = 'block'; // Revert to default display property
            console.log('Sidebar shown');
        }

        // Set margin-left of .content to 250px on all other pages
        const content = document.querySelector('.content');
        if (content) {
            content.style.marginLeft = '250px'; // Set margin-left to 250px
            console.log('Content margin-left set to 250px');
        }
    } else {
        console.log('Path matches index.html, login.html, or register');
        // Hide the sidebar on index.html, login.html, or register
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.display = 'none'; // Hide the sidebar
            console.log('Sidebar hidden');
        }

        // Reset margin-left of .content on index.html, login.html, or register
        const content = document.querySelector('.content');
        if (content) {
            content.style.marginLeft = '0px'; // Reset margin-left
            console.log('Content margin-left reset to 0px');
        }
    }
});