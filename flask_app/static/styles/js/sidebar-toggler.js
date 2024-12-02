function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar-wrapper');
    sidebar.classList.toggle('collapsed');
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('collapsed');
    /*
    const navbar = document.querySelector('.navbar-instructor-view');
    navbar.classList.toggle('collapsed');
    */
}