console.log('Document loaded'); // Check if this prints

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired'); // Check if this prints

    // Function to toggle sidebar
    function toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            if (sidebar.style.display === 'block') {
                sidebar.style.display = 'none'; // Hide the sidebar
                console.log('Sidebar hidden');
            } else {
                sidebar.style.display = 'block'; // Show the sidebar
                console.log('Sidebar shown');
            }
        }
    }

    // Event listener for navbar toggler button
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', toggleSidebar);
        console.log('Navbar toggler click event listener added');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired'); // Check if this prints

    // Get the current path
    const path = window.location.pathname;
    console.log('Current path:', path); // Check if this prints

    // Check if the current path is 'index.html' or 'login.html' (or their equivalents)
    if (!(path === "/index.html" || path === "/login.html" || path === "/index" || path === "/login")) {
        console.log('Path does not match index.html or login.html');

        // Show the sidebar on all other pages
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.display = 'block'; // Revert to default display property
            console.log('Sidebar shown');
        }

        // Set margin-left of .content to 0px on all other pages
        const content = document.querySelector('.content');
        if (content) {
            content.style.marginLeft = '250px'; // Set margin-left to 0px
            console.log('Content margin-left set to 0px');
        }

        // Show the navbar-toggler on all other pages
        const sidebarMenuButton = document.querySelector('.sidebar-menu-button');
        if (sidebarMenuButton) {
            sidebarMenuButton.style.display = 'block'; // or manipulate classes
            console.log('Sidebar menu button shown');
        }
    }
});