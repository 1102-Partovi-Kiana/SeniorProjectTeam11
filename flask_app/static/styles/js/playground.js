document.addEventListener('DOMContentLoaded', () => {

    const videos = document.querySelectorAll('.playground-card-video');
    
    videos.forEach(video => {
        video.autoplay = true;  
        video.muted = true;      
        video.loop = true;   
        video.playsInline = true; 
        video.disablePictureInPicture = true;
    
        video.style.width = '100%';
        video.style.maxWidth = '360px';
        video.style.height = '200px';
        video.style.objectFit = 'cover';
        video.style.borderRadius = '10px';
        video.style.boxShadow = '0px 4px 12px rgba(0, 0, 0, 0.1)';
        
        video.removeAttribute('controls');
    });
});
