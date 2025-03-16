// Theme Toggle
const themeSwitch = document.getElementById('theme-switch');
const body = document.body;

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    body.classList.add('light-theme');
    themeSwitch.checked = true;
}

// Theme switch handler
themeSwitch.addEventListener('change', () => {
    if (themeSwitch.checked) {
        body.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('light-theme');
        localStorage.setItem('theme', 'dark');
    }
});

// Skill Percentage Animation
const badges = document.querySelectorAll('.badge');

// Intersection Observer for triggering animations when badges are in view
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const badge = entry.target;
            const percentage = badge.getAttribute('data-percentage');
            
            // Set the percentage as a CSS custom property
            badge.style.setProperty('--percentage', percentage + '%');
            badge.classList.add('animated');
            
            // Start the counter animation
            animateCounter(badge, percentage);
            
            // Stop observing once animated
            observer.unobserve(badge);
        }
    });
}, {
    threshold: 0.5
});

// Observe all badges
badges.forEach(badge => {
    observer.observe(badge);
});

// Counter animation function
function animateCounter(badge, targetPercentage) {
    let currentPercentage = 0;
    const duration = 1500; // 1.5 seconds
    const interval = 16; // ~60fps
    const steps = duration / interval;
    const increment = targetPercentage / steps;
    
    const animation = setInterval(() => {
        currentPercentage += increment;
        
        if (currentPercentage >= targetPercentage) {
            currentPercentage = targetPercentage;
            clearInterval(animation);
        }
        
        // Update the badge's content
        const displayValue = Math.round(currentPercentage);
        const originalText = badge.textContent.split(' ')[0];
        badge.textContent = `${originalText} ${displayValue}%`;
    }, interval);
}
