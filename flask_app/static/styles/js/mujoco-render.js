document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('mujoco-canvas');
    const ctx = canvas.getContext('2d');
    const mujocoFeedUrl = '/mujoco-feed';

    function startMujocoStream() {
        const img = new Image();
        img.src = mujocoFeedUrl;

        img.onload = function() {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        
        setTimeout(startMujocoStream, 100); // Adjust the interval as needed
    }

    startMujocoStream();
});
