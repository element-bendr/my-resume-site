// Enhanced particles configuration with adjustments for both themes

window.addEventListener('load', function() {
    setTimeout(function() {
        if (typeof particlesJS !== 'function') return;
        
        const isDarkMode = document.body.classList.contains('dark-mode');
        
        particlesJS('particles-js', {
            "particles": {
                "number": {
                    "value": isDarkMode ? 100 : 70, // More particles in dark mode for better visibility
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": isDarkMode ? 
                        ["#ffffff", "#77c1ff", "#7dabf5", "#aa88ff"] : // Multi-color in dark mode
                        ["#4285F4", "#34A8EB", "#9C27B0", "#E91E63"]  // Colorful in light mode
                },
                "shape": {
                    "type": ["circle", "triangle"], // Mix of shapes for visual interest
                    "stroke": {
                        "width": 0
                    },
                    "polygon": {
                        "nb_sides": 5
                    }
                },
                "opacity": {
                    "value": isDarkMode ? 0.5 : 0.3, // Higher opacity in dark mode
                    "random": true, // Random opacity for depth
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
                    "distance": isDarkMode ? 150 : 120, // Longer connections in dark mode
                    "color": isDarkMode ? "#ffffff" : "#4a90e2",
                    "opacity": isDarkMode ? 0.4 : 0.2,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": isDarkMode ? 2 : 1.5, // Slightly faster in dark mode
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": true, // Particles slightly attract each other
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
                        "mode": "bubble" // Particles expand on hover
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push" // Add particles on click
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 180,
                        "line_linked": {
                            "opacity": 0.8
                        }
                    },
                    "bubble": {
                        "distance": 200,
                        "size": 6, // Expand particles on hover
                        "duration": 0.3,
                        "opacity": isDarkMode ? 0.8 : 0.6,
                        "speed": 3
                    },
                    "repulse": {
                        "distance": 200,
                        "duration": 0.4
                    },
                    "push": {
                        "particles_nb": 4
                    }
                }
            },
            "retina_detect": true
        });
        
        // Add theme change listener to update particles
        document.getElementById('theme-toggle')?.addEventListener('change', function() {
            // Wait for theme to change
            setTimeout(function() {
                // Reload particles with new theme settings
                const isDarkMode = document.body.classList.contains('dark-mode');
                refreshParticles(isDarkMode);
            }, 300);
        });
    }, 300);
});

// Function to refresh particles with current theme
function refreshParticles(isDarkMode) {
    if (typeof pJSDom !== 'undefined' && pJSDom.length > 0) {
        try {
            pJSDom[0].pJS.fn.vendors.destroypJS();
            setTimeout(function() {
                // Re-trigger the main initialization with new theme
                window.dispatchEvent(new Event('load'));
            }, 100);
        } catch (e) {
            console.error("Error refreshing particles:", e);
        }
    }
}