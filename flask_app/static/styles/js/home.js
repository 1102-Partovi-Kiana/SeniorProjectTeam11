document.addEventListener('DOMContentLoaded', () => {
    const square = document.getElementById('animatedSquare');
    const cards = document.querySelectorAll('.card');

    square.style.backgroundImage = 'linear-gradient(45deg, #007bff, #007bff)';

    void square.offsetWidth;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                console.log("Square in view - adding 'expand' class");
                square.classList.add('expand'); 

                square.addEventListener('transitionend', () => {
                    console.log("Square animation complete - adding 'reveal-cards' class to each card");

                    cards.forEach((card, index) => {
                        setTimeout(() => {
                            console.log(`Revealing card ${index + 1}`);
                            card.classList.add('reveal-cards'); 
                        }, index * 200); 
                    });
                }, { once: true });

                observer.unobserve(square); 
            }
        });
    }, { threshold: 0.5 });

    observer.observe(square);
});