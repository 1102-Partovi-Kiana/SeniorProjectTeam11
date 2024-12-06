document.addEventListener('DOMContentLoaded', () => {
    
    console.log("DOM is ready.");

    const square = document.getElementById('animatedSquare'); 
    const cards = document.querySelectorAll('.homepage-card'); 
    const section = document.querySelector('.open-source-section');

    console.log("Variables are ready:", {
        square,
        cards,
        section
    });

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {

            if (entry.isIntersecting) { 
                console.log(".open-source-section is in view, beginning the animations.");

                square.classList.add('animate');

                setTimeout(() => {
                    cards.forEach((card, index) => {
                        setTimeout(() => {
                            card.classList.add('reveal-cards'); 
                        }, index * 200); 
                    });
                }, 1500); 

                observer.unobserve(section);

            } else {
                console.log(".open-source-section is not in view yet.");
            }
        });
    }, { threshold: 0.5 }); 

    observer.observe(section);
});
