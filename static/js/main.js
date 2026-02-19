const navbar = document.getElementById('navbar');

function handleScroll() {
    if (!navbar) {
        console.log('Missing!')
        return;
    } // prevent error if navbar is missing
    if (window.scrollY === 0) {
        navbar.classList.add('no-shadow');
    } else {
        navbar.classList.remove('no-shadow');
    }
}

handleScroll();
window.addEventListener('scroll', handleScroll);
