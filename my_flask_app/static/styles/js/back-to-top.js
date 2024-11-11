document.addEventListener("DOMContentLoaded", () => {
    const backToTopButton = document.getElementById("backToTop");

    function isBottomOfPage() {
        return window.innerHeight + window.scrollY >= document.body.offsetHeight - 10;
    }

    window.addEventListener("scroll", () => {
        if (isBottomOfPage()) {
            backToTopButton.classList.add("show");
            backToTopButton.classList.remove("hide");
        } else {
            backToTopButton.classList.add("hide");
            backToTopButton.classList.remove("show");
        }
    });

    backToTopButton.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});
