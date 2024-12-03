document.getElementById("playButton").addEventListener("click", function () {

    const video = document.getElementById("videoPlayer");
    const playButton = this;

    if (video.paused) {
        video.play();
        playButton.style.display = "none";
    } else {
        video.pause();
        playButton.style.display = "block";
    }

});

document.getElementById("videoPlayer").addEventListener("ended", function () {

    const playButton = document.getElementById("playButton");
    playButton.style.display = "block"; 

});

document.addEventListener("keydown", function (event) {
    
    const video = document.getElementById("videoPlayer");
    const playButton = document.getElementById("playButton");

    if (event.code === "Space") {
        event.preventDefault();

        if (playButton.style.display !== "none") {
            video.play();
            playButton.style.display = "none";
        } else {
            if (video.paused) {
                video.play();
            } else {
                video.pause();
            }
        }
    }
});
