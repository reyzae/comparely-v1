// ==========================================
// HEADER SCROLL ENHANCEMENT
// Enhanced shadow effect saat scroll (mobile)
// ==========================================

document.addEventListener('DOMContentLoaded', function () {
    const header = document.querySelector('.header');

    if (!header) return;

    // Detect scroll untuk enhanced shadow
    let lastScrollTop = 0;
    let ticking = false;

    function updateHeaderShadow() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Add stronger shadow when scrolled
        if (scrollTop > 10) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        lastScrollTop = scrollTop;
        ticking = false;
    }

    // Use requestAnimationFrame for smooth performance
    window.addEventListener('scroll', function () {
        if (!ticking) {
            window.requestAnimationFrame(updateHeaderShadow);
            ticking = true;
        }
    });
});
