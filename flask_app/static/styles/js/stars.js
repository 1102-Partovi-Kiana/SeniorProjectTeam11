document.querySelector('.page-header').addEventListener('mouseenter', () => {
    
    const header = document.querySelector('.page-header');

    if (!header) {
        console.error('Could not find header element');
        return;
    }

    for (let i = 0; i < 19; i++) {
        const star = document.createElement('div');
        star.classList.add('star');

        // Randomize stars positioning
        const randomTop = Math.random() * 100;
        const randomLeft = Math.random() * 100;

        // Randomize stars sizing
        const minSize = 0.5;
        const maxSize = 2;
        const randomSize = (minSize + Math.random() * (maxSize - minSize)).toFixed(2);

        // Randomize stars movement
        const randomX = Math.random();
        const randomY = Math.random();

        star.style.top = `${randomTop}%`;
        star.style.left = `${randomLeft}%`;
        star.style.setProperty('--random-x', randomX);
        star.style.setProperty('--random-y', randomY);
        star.style.setProperty('--star-size', randomSize);

        header.appendChild(star);

        // After animation is done, we need to remove the stars
        setTimeout(() => {
            try {
                star.remove();
            } catch (err) {
                console.error('Error with removing stars:', err);
            }
        }, 4000); // 4 seconds
    }
});