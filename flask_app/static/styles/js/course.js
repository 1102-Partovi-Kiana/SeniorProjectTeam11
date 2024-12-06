document.querySelectorAll('.sub-list a').forEach(link => {

    link.addEventListener('click', function () {
        document.querySelectorAll('.sub-list a').forEach(item => item.classList.remove('active'));
        this.classList.add('active');
    });
    
});
