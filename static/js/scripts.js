console.log('Document loaded'); // Check if this prints

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired'); // Check if this prints

    // Function to toggle sidebar


    // Get the current path
    const path = window.location.pathname;
    console.log('Current path:', path); // Check if this prints

    // Check if the current path is not 'index.html' or 'login.html' (or their equivalents)
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

        // Show the sidebar-menu-button on all other pages
        const sidebarMenuButton = document.querySelector('.sidebar-menu-button');
        if (sidebarMenuButton) {
            sidebarMenuButton.style.display = 'block'; // or manipulate classes
            console.log('Sidebar menu button shown');
        }
    }
});
