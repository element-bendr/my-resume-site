// Create wave container
function createWaveContainer() {
  const waveContainer = document.createElement('div');
  waveContainer.className = 'wave-container';
  
  // Create three waves
  for (let i = 0; i < 3; i++) {
    const wave = document.createElement('div');
    wave.className = 'wave';
    waveContainer.appendChild(wave);
  }
  
  document.body.appendChild(waveContainer);
}

// Initialize Particles.js with enhanced configuration
particlesJS('particles-js', {
  "particles": {
    "number": {
      "value": 60,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": {
      "value": ["#6366f1", "#ec4899", "#3b82f6", "#f43f5e", "#8b5cf6"]
    },
    "shape": {
      "type": "circle"
    },
    "opacity": {
      "value": 0.6,
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
        "size_min": 0.1,
        "sync": false
      }
    },
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#ffffff",
      "opacity": 0.15,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 1.5,
      "direction": "none",
      "random": true,
      "straight": false,
      "out_mode": "bounce",
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
          "opacity": 0.5
        }
      },
      "push": {
        "particles_nb": 3
      }
    }
  },
  "retina_detect": true
});

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Create wave animation
  createWaveContainer();
  
  // Update particle colors based on theme
  function updateParticleColors(isLight) {
    const colors = isLight 
      ? ["#6366f1", "#ec4899", "#3b82f6", "#f43f5e", "#8b5cf6"].map(color => adjustColorBrightness(color, -20))
      : ["#6366f1", "#ec4899", "#3b82f6", "#f43f5e", "#8b5cf6"];
    
    if (window.pJSDom && window.pJSDom[0]) {
      const particleSystem = window.pJSDom[0].pJS;
      particleSystem.particles.array.forEach(particle => {
        particle.color.value = colors[Math.floor(Math.random() * colors.length)];
        particle.color.rgb = hexToRgb(particle.color.value);
      });
      particleSystem.particles.line_linked.color = isLight ? "#2c3e50" : "#ffffff";
      particleSystem.particles.line_linked.color_rgb_line = hexToRgb(particleSystem.particles.line_linked.color);
      particleSystem.fn.particlesRefresh();
    }
  }

  // Helper function to convert hex to RGB
  function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  }

  // Helper function to adjust color brightness
  function adjustColorBrightness(hex, percent) {
    const rgb = hexToRgb(hex);
    const adjust = (value) => {
      return Math.max(0, Math.min(255, Math.round(value * (1 + percent/100))));
    };
    return `#${[adjust(rgb.r), adjust(rgb.g), adjust(rgb.b)]
      .map(x => x.toString(16).padStart(2, '0')).join('')}`;
  }

  // Listen for theme changes
  const themeSwitch = document.getElementById('theme-switch');
  themeSwitch.addEventListener('change', (e) => {
    updateParticleColors(e.target.checked);
  });

  // Initial color setup based on saved theme
  const initialTheme = localStorage.getItem('theme') === 'light';
  updateParticleColors(initialTheme);
});

// Error handling
window.onerror = function(msg, url, lineNo, columnNo, error) {
  console.error('Particles/Wave Error:', msg, 'at', url, lineNo, columnNo, error);
  return false;
};
