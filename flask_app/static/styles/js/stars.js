document.querySelector('.page-header').addEventListener('mouseenter', () => {
    const header = document.querySelector('.page-header');

    for (let i = 0; i < 20; i++) { // Generate 20 stars
        const star = document.createElement('div');
        star.classList.add('star');

        // Randomize position, size, and movement
        star.style.top = `${Math.random() * 100}%`;
        star.style.left = `${Math.random() * 100}%`;
        star.style.setProperty('--random-x', Math.random()); // Random X movement
        star.style.setProperty('--random-y', Math.random()); // Random Y movement
        star.style.setProperty('--star-size', (0.5 + Math.random() * 1.5).toFixed(2)); // Random size between 0.5 and 2

        header.appendChild(star);

        // Remove star after animation ends
        setTimeout(() => {
            star.remove();
        }, 4000); // Matches animation duration
    }
});
