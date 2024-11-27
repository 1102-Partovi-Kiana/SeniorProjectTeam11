document.addEventListener('DOMContentLoaded', () => {
    const square = document.getElementById('animatedSquare');
    const cards = document.querySelectorAll('.homepage-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                console.log("Square is in view, starting animation.");
                square.classList.add('expand');

                setTimeout(() => {
                    console.log("Manually triggering card reveal.");
                    cards.forEach((card, index) => {
                        setTimeout(() => {
                            console.log(`Revealing card ${index + 1}`);
                            card.classList.add('reveal-cards'); 
                        }, index * 200);
                    });
                }, 1500); 

                observer.unobserve(square); 
            }
        });
    }, { threshold: 0.5 });

    observer.observe(square);
});
