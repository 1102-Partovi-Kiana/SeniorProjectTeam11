
let index = 0;

function moveSlide(step) {
    const slider = document.querySelector(".image-slider");
    const images = document.querySelectorAll(".slider-image");
    const totalNumberOfImages = images.length;

    index += step;

    if (index >= totalNumberOfImages) index = 0;
    if (index < 0) index = totalNumberOfImages - 1;

    const offset = -index * 100; 
    slider.style.transform = `translateX(${offset}%)`;
}

