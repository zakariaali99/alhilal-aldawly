document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.getElementById('main-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                header.classList.add('scrolled');
                header.querySelector('.navbar').classList.add('py-2');
                header.querySelector('.navbar').classList.remove('py-3');
            } else {
                header.classList.remove('scrolled');
                header.querySelector('.navbar').classList.add('py-3');
                header.querySelector('.navbar').classList.remove('py-2');
            }
        });
    }

    // GSAP Hero Animations (Only for active slide)
    if (typeof gsap !== 'undefined') {
        const activeSlide = document.querySelector('.carousel-item.active');
        if (activeSlide) {
            gsap.from(activeSlide.querySelectorAll('.reveal-text'), {
                y: 50,
                opacity: 0,
                duration: 1,
                ease: "power3.out"
            });

            gsap.from(activeSlide.querySelectorAll('.reveal-p'), {
                y: 30,
                opacity: 0,
                duration: 1,
                delay: 0.3,
                ease: "power3.out"
            });

            gsap.from(activeSlide.querySelectorAll('.reveal-btn'), {
                y: 20,
                opacity: 0,
                duration: 0.8,
                delay: 0.6,
                ease: "power3.out"
            });
        }

        // Animate on slide change
        const carousel = document.getElementById('heroCarousel');
        if (carousel) {
            carousel.addEventListener('slid.bs.carousel', function (event) {
                const newActive = event.relatedTarget;
                gsap.from(newActive.querySelectorAll('.reveal-text'), {
                    y: 50,
                    opacity: 0,
                    duration: 1,
                    ease: "power3.out"
                });
                gsap.from(newActive.querySelectorAll('.reveal-p'), {
                    y: 30,
                    opacity: 0,
                    duration: 1,
                    delay: 0.3,
                    ease: "power3.out"
                });
                gsap.from(newActive.querySelectorAll('.reveal-btn'), {
                    y: 20,
                    opacity: 0,
                    duration: 0.8,
                    delay: 0.6,
                    ease: "power3.out"
                });
            });
        }
    }

    // Intersection Observer for Animate on Scroll
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // Reading Progress Bar
    const progress = document.querySelector('.reading-progress');
    if (progress) {
        window.addEventListener('scroll', () => {
            const h = document.documentElement;
            const b = document.body;
            const st = 'scrollTop';
            const sh = 'scrollHeight';
            const percent = (h[st] || b[st]) / ((h[sh] || b[sh]) - h.clientHeight) * 100;
            progress.style.width = percent + '%';
        });
    }
});
