function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar-wrapper');
    sidebar.classList.toggle('collapsed');
    const dashboard_table = document.querySelector('.dashboard-table-container');
    dashboard_table.classList.toggle('collapsed');
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('collapsed');
    const footer = document.querySelector('.footer');
    footer.classList.toggle('collapsed');
    /*
    const navbar = document.querySelector('.navbar-instructor-view');
    navbar.classList.toggle('collapsed');
    */
}