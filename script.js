document.addEventListener('DOMContentLoaded', () => {
    // Initialize dark mode from localStorage
    const initializeTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
            document.getElementById('theme-toggle').checked = true;
        }
    };

    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
        }
    });

    // Animate progress bars
    const animateProgressBars = () => {
        const progressBars = document.querySelectorAll('.progress');
        progressBars.forEach(progress => {
            const targetWidth = progress.getAttribute('data-progress') + '%';
            progress.style.width = '0%';
            setTimeout(() => {
                progress.style.width = targetWidth;
            }, 100);
        });
    };

    // Intersection Observer for scroll animations
    const observeElements = () => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    if (entry.target.classList.contains('skills')) {
                        animateProgressBars();
                    }
                }
            });
        }, {
            threshold: 0.1
        });

        // Observe all glass cards
        document.querySelectorAll('.glass-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });
    };

    // Initialize theme and animations
    initializeTheme();
    observeElements();

    // Add hover effect for social icons
    document.querySelectorAll('.social-icon').forEach(icon => {
        icon.addEventListener('mouseover', () => {
            icon.style.color = getComputedStyle(document.documentElement)
                .getPropertyValue('--progress-fill').trim();
        });
        icon.addEventListener('mouseout', () => {
            icon.style.color = getComputedStyle(document.documentElement)
                .getPropertyValue('--text-primary').trim();
        });
    });

    // Optional: Add smooth scroll for better UX
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
