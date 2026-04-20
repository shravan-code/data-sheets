/**
 * Main Application Logic
 * Core functionality for the Data Sheets website
 */

// Theme Management
class ThemeManager {
    constructor() {
        this.STORAGE_KEY = 'datasheet-theme';
        this.DARK_CLASS = 'dark';
        this.init();
    }

    init() {
        const savedTheme = localStorage.getItem(this.STORAGE_KEY);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedTheme) {
            this.setTheme(savedTheme);
        } else if (prefersDark) {
            this.setTheme('dark');
        }

        this.setupListener();
    }

    setTheme(theme) {
        const isDark = theme === 'dark';
        if (isDark) {
            document.documentElement.classList.add(this.DARK_CLASS);
        } else {
            document.documentElement.classList.remove(this.DARK_CLASS);
        }
        localStorage.setItem(this.STORAGE_KEY, theme);
    }

    toggle() {
        const isDark = document.documentElement.classList.contains(this.DARK_CLASS);
        this.setTheme(isDark ? 'light' : 'dark');
    }

    setupListener() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }
    }
}

// Mobile Menu Manager
class MobileMenuManager {
    constructor() {
        this.menuBtn = document.getElementById('mobile-menu-btn');
        this.mobileMenu = document.getElementById('mobile-menu');
        this.init();
    }

    init() {
        if (!this.menuBtn || !this.mobileMenu) return;

        this.menuBtn.addEventListener('click', () => this.toggle());

        // Close menu when clicking links
        this.mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => this.close());
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.menuBtn.contains(e.target) && !this.mobileMenu.contains(e.target)) {
                this.close();
            }
        });
    }

    toggle() {
        this.mobileMenu.classList.toggle('hidden');
        this.menuBtn.classList.toggle('rotate-180');
    }

    close() {
        this.mobileMenu.classList.add('hidden');
        this.menuBtn.classList.remove('rotate-180');
    }
}

// Smooth Scroll
class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }
}

// Intersection Observer for animations
class AnimationObserver {
    constructor() {
        this.init();
    }

    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('[data-animate]').forEach(el => {
            observer.observe(el);
        });
    }
}

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    new MobileMenuManager();
    new SmoothScroll();
    new AnimationObserver();

    console.log('✓ Data Sheets App initialized');
});
