document.addEventListener('DOMContentLoaded', function () {
    const coreCertCloseButton = document.getElementById('core-cert-close-button');
    const coreCertPopup = document.getElementById('core-certificate-popup');

    if (coreCertCloseButton && coreCertPopup) {
        coreCertCloseButton.addEventListener('click', function () {
            // Debug logging to confirm the click is detected, had problems with it earlier
            console.log("Close button clicked.");
            coreCertPopup.style.display = 'none';
        });
    } else {
        console.error("Popup or close button element not found.");
    }
});
