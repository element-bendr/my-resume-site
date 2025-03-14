// Clean implementation of JavaScript functions

// Theme toggle initialization
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;
    
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && prefersDarkScheme.matches)) {
        document.body.classList.add('dark-mode');
        themeToggle.checked = true;
    }
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
        
        // Refresh particles when theme changes
        setTimeout(() => {
            refreshParticles();
        }, 300);
    });
}

// Initialize particles
function initParticles() {
    console.log("Initializing particles...");
    
    if (typeof particlesJS !== 'function') {
        console.error('particles.js not loaded');
        return;
    }
    
    const isDarkMode = document.body.classList.contains('dark-mode');
    console.log("Initializing particles. Dark mode:", isDarkMode);
    
    try {
        // Basic configuration that works reliably
        particlesJS("particles-js", {
            "particles": {
                "number": {
                    "value": isDarkMode ? 100 : 70,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": isDarkMode ? 
                        ["#ffffff", "#77c1ff", "#7dabf5"] : 
                        ["#4285F4", "#34A8EB", "#9C27B0"]
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0
                    }
                },
                "opacity": {
                    "value": isDarkMode ? 0.5 : 0.3,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 2,
                        "size_min": 0.3,
                        "sync": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": isDarkMode ? 150 : 120,
                    "color": isDarkMode ? "#ffffff" : "#4a90e2",
                    "opacity": isDarkMode ? 0.4 : 0.2,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": isDarkMode ? 2 : 1.5,
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": true,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "grab"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 140,
                        "line_linked": {
                            "opacity": 1
                        }
                    },
                    "push": {
                        "particles_nb": 4
                    }
                }
            },
            "retina_detect": true
        });
        
        console.log("Particles initialized successfully");
        
        // Create wave background after particles are initialized
        setTimeout(() => {
            addWaveBackground(isDarkMode);
        }, 200);
    } catch (e) {
        console.error("Error initializing particles:", e);
    }
}

// Function to refresh particles (used when changing themes)
function refreshParticles() {
    console.log("Refreshing particles...");
    
    try {
        // Remove old wave canvas if it exists
        const oldWaveCanvas = document.getElementById('wave-canvas');
        if (oldWaveCanvas) {
            oldWaveCanvas.remove();
        }
        
        // Remove any existing particle canvas
        const oldCanvas = document.querySelector('.particles-js-canvas-el');
        if (oldCanvas) {
            oldCanvas.remove();
        }
        
        // Clear the particles-js div
        const container = document.getElementById('particles-js');
        if (container) {
            container.innerHTML = '';
        }
        
        // Reinitialize particles from scratch
        setTimeout(() => {
            initParticles();
        }, 100);
    } catch (e) {
        console.error("Error refreshing particles:", e);
    }
}

// Add wave background with proper z-index and enhanced colors
function addWaveBackground(isDarkMode) {
    console.log("Adding wave background. Dark mode:", isDarkMode);
    
    // Remove existing wave canvas if present
    const existingCanvas = document.getElementById('wave-canvas');
    if (existingCanvas) {
        existingCanvas.remove();
    }
    
    // Create wave canvas
    const canvas = document.createElement('canvas');
    canvas.id = 'wave-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '-2';
    
    // Add canvas to body before particles-js for proper stacking
    const particlesDiv = document.getElementById('particles-js');
    if (particlesDiv) {
        document.body.insertBefore(canvas, particlesDiv);
    } else {
        document.body.prepend(canvas);
    }
    
    // Get canvas context and set dimensions
    const ctx = canvas.getContext('2d');
    const resize = () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    };
    resize();
    
    // Enhanced wave colors with higher saturation
    const darkModeWaveColors = [
        'rgba(41, 98, 255, 0.12)',    // Deep blue
        'rgba(103, 58, 183, 0.10)',   // Purple
        'rgba(170, 0, 255, 0.08)',    // Vibrant purple
        'rgba(0, 149, 255, 0.07)'     // Bright blue
    ];
    
    // Light mode wave colors with slightly better visibility
    const lightModeWaveColors = [
        'rgba(66, 133, 244, 0.06)',   // Google blue
        'rgba(52, 168, 235, 0.05)',   // Sky blue
        'rgba(156, 39, 176, 0.04)',   // Purple
        'rgba(233, 30, 99, 0.03)'     // Pink
    ];
    
    // Select colors based on theme
    const waveColors = isDarkMode ? darkModeWaveColors : lightModeWaveColors;
    
    // Wave animation settings with more variety
    const waves = [
        {
            y: canvas.height * 0.60,
            length: 0.01,
            amplitude: 50,
            frequency: 0.01,
            color: waveColors[0],
            speed: 0.05
        },
        {
            y: canvas.height * 0.55,
            length: 0.015,
            amplitude: 40,
            frequency: 0.02,
            color: waveColors[1],
            speed: 0.07
        },
        {
            y: canvas.height * 0.65,
            length: 0.02,
            amplitude: 30,
            frequency: 0.015,
            color: waveColors[2],
            speed: 0.03
        },
        {
            y: canvas.height * 0.70,
            length: 0.01,
            amplitude: 25,
            frequency: 0.025,
            color: waveColors[3],
            speed: 0.06
        }
    ];
    
    // Animation variables
    let increment = 0;
    
    // Improved animate function with smoother waves
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw waves with refined curves
        waves.forEach(wave => {
            ctx.beginPath();
            ctx.moveTo(0, wave.y);
            
            // Draw wave with more detailed points for smoother curves
            for (let i = 0; i < canvas.width; i += 5) {
                ctx.lineTo(
                    i, 
                    wave.y + Math.sin(i * wave.length + increment * wave.frequency) * wave.amplitude * 
                    (1 + Math.sin(increment * 0.003) * 0.1) // Add subtle variation over time
                );
            }
            
            ctx.lineTo(canvas.width, canvas.height);
            ctx.lineTo(0, canvas.height);
            ctx.closePath();
            ctx.fillStyle = wave.color;
            ctx.fill();
            
            // Update wave position for next frame with individual speeds
            wave.y += Math.sin(increment * 0.02) * 0.1; // Subtle vertical movement
        });
        
        // Increment with requestAnimationFrame timing for smoother animation
        increment += 1;
        requestAnimationFrame(animate);
    }
    
    // Start animation
    animate();
    
    // Better window resize handling with debounce
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            resize();
            
            // Redistribute waves on resize for better positioning
            waves.forEach((wave, index) => {
                wave.y = canvas.height * (0.55 + index * 0.05);
            });
        }, 100);
    });
}

// Initialize animations for interactive elements
function initAnimations() {
    const elements = document.querySelectorAll('.icon-animate');
    elements.forEach(element => {
        element.style.opacity = '1';
    });
}

// Add button to refresh animations
function createRefreshButton() {
    const button = document.getElementById('refresh-animations');
    if (button) return; // Don't create if already exists
    
    const refreshBtn = document.createElement('button');
    refreshBtn.id = 'refresh-animations';
    refreshBtn.textContent = '🔄 Refresh';
    refreshBtn.setAttribute('title', 'Refresh animations and particles');
    document.body.appendChild(refreshBtn);
    
    refreshBtn.addEventListener('click', () => {
        // Restart animations
        const elements = document.querySelectorAll('.icon-animate');
        elements.forEach(element => {
            element.style.animation = 'none';
            setTimeout(() => {
                element.style.animation = '';
            }, 10);
        });
        
        // Refresh particles
        refreshParticles();
    });
}

// Enhanced skill badge interactions
function addSkillCardInteraction() {
    const badges = document.querySelectorAll('.badge');
    
    badges.forEach((badge, index) => {
        // Initial state - start invisible
        badge.style.opacity = '0';
        badge.style.transform = 'translateY(20px)';
        
        // Animate in with staggered delay
        setTimeout(() => {
            badge.style.opacity = '1';
            badge.style.transform = 'translateY(0)';
        }, 100 + index * 50); // Stagger the animations
        
        // Enhanced hover effect with subtle 3D tilt
        badge.addEventListener('mousemove', (e) => {
            const rect = badge.getBoundingClientRect();
            const x = e.clientX - rect.left; 
            const y = e.clientY - rect.top;
            
            // Calculate rotation based on cursor position
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateY = (x - centerX) / 15;  // Reduced intensity for subtle effect
            const rotateX = (centerY - y) / 15;  // Reduced intensity for subtle effect
            
            // Apply 3D tilt effect
            badge.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });
        
        // Reset on mouse leave
        badge.addEventListener('mouseleave', () => {
            badge.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale(1)';
        });
    });
}

// Reading progress indicator
function initReadingProgress() {
    const progressBar = document.querySelector('.reading-progress');
    const sections = document.querySelectorAll('section.glass-card');
    const sectionDots = document.querySelectorAll('.section-dot');
    
    // Clear any active state on page load/refresh
    sectionDots.forEach(dot => {
        dot.classList.remove('active');
    });
    
    // Set the first dot as active initially
    if (sectionDots.length > 0) {
        sectionDots[0].classList.add('active');
    }
    
    // Update section indicators on scroll
    window.addEventListener('scroll', () => {
        // Update reading progress
        const windowHeight = window.innerHeight;
        const fullHeight = document.body.offsetHeight - windowHeight;
        const scrolled = window.scrollY;
        const progress = (scrolled / fullHeight) * 100;
        
        if (progressBar) {
            progressBar.style.height = `${progress}%`;
        }
        
        // Update active section dot
        let currentSectionIndex = 0;
        let closestSection = Infinity;
        
        sections.forEach((section, index) => {
            const rect = section.getBoundingClientRect();
            const distance = Math.abs(rect.top - windowHeight/2);
            
            // Find the section closest to the middle of the viewport
            if (distance < closestSection) {
                closestSection = distance;
                currentSectionIndex = index;
            }
        });
        
        // Update the active dot
        sectionDots.forEach((dot, index) => {
            if (index === currentSectionIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    });
    
    // Enhanced click event for section dots
    sectionDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            // Scroll to section
            if (sections[index]) {
                sections[index].scrollIntoView({
                    behavior: 'smooth'
                });
            }
            
            // Visually update the active dot immediately
            sectionDots.forEach((d) => {
                d.classList.remove('active');
            });
            dot.classList.add('active');
        });
    });
}

// Back to top button functionality
function addBackToTopButton() {
    // Create the button if it doesn't already exist
    if (!document.getElementById('back-to-top')) {
        const button = document.createElement('button');
        button.id = 'back-to-top';
        button.innerHTML = '&uarr;';
        button.setAttribute('aria-label', 'Back to top');
        button.setAttribute('title', 'Back to top');
        document.body.appendChild(button);
    }
    
    const button = document.getElementById('back-to-top');
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > window.innerHeight * 0.5) {
            button.classList.add('visible');
        } else {
            button.classList.remove('visible');
        }
    });
    
    // Scroll to top with smooth behavior
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Function to animate progress bars when they enter the viewport
function initProgressBars() {
    // Function to check if element is in viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    }
    
    // Get all progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    
    // Function to animate visible progress bars
    function animateVisibleBars() {
        progressBars.forEach(bar => {
            if (isInViewport(bar) && !bar.classList.contains('animated')) {
                const computedStyle = window.getComputedStyle(bar);
                const width = computedStyle.getPropertyValue('width');
                
                // First set width to 0
                bar.style.width = '0';
                
                // Then animate to the target width
                setTimeout(() => {
                    bar.style.width = width;
                    bar.classList.add('animated');
                }, 100);
            }
        });
    }
    
    // Run once on load
    animateVisibleBars();
    
    // Run on scroll
    window.addEventListener('scroll', animateVisibleBars);
}

// Initialize everything when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded");
    
    // Create particles container if it doesn't exist
    if (!document.getElementById('particles-js')) {
        const particlesDiv = document.createElement('div');
        particlesDiv.id = 'particles-js';
        document.body.prepend(particlesDiv);
    }
    
    // Initialize components
    initThemeToggle();
    initAnimations();
    createRefreshButton();
    initReadingProgress();
    addBackToTopButton();
    
    // Add skill card interactions
    if (window.innerWidth > 768) { // Only on desktop
        addSkillCardInteraction();
    }
    
    // Initialize progress bar animations
    initProgressBars();
    
    // Initialize particles last
    setTimeout(() => {
        console.log("Initializing particles");
        initParticles();
    }, 300);
});