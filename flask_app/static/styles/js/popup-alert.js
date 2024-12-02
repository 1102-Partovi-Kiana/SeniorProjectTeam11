document.addEventListener('DOMContentLoaded', function() {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(toastEl) {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    });
});