
document.addEventListener('DOMContentLoaded', function() {
    const toastContainer = document.querySelector('.toast-container');
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach(function(toastEl, index) {
        const toast = new bootstrap.Toast(toastEl);
        
        // Set the top position for each toast
        const topOffset = 20 + index * 140;  // 20px for the first toast, 100px for the second, etc.
        toastEl.style.top = `${topOffset}px`;

        // Show the toast
        toast.show();

        // Remove the toast after 5 seconds
        setTimeout(function() {
            toastEl.remove();

            // Check if there are no more toasts and remove the container
            if (toastContainer.querySelectorAll('.toast').length === 0) {
                toastContainer.remove();
            }
        }, 5000);  // 5000 milliseconds (5 seconds)
    });
});
