// Look for .hamburger
var hamburger = document.querySelector(".hamburger");
// On click
hamburger.addEventListener("click", function () {
    // Toggle class "is-active"
    hamburger.classList.toggle("is-active");
    // Log when the hamburger is clicked
    console.log("Hamburger clicked!");
    // Log if the "is-active" class is toggled
    if (hamburger.classList.contains("is-active")) {
        console.log("Hamburger is now active");
    } else {
        console.log("Hamburger is now inactive");
    }
    // Do something else, like open/close menu
});