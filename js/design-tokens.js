/**
 * Design Tokens Module
 * Loads and manages colors, fonts, and theme-related CSS variables
 * Used across all pages for consistent theming
 */

const DesignTokens = (function() {
    'use strict';

    const TOKENS = {
        colors: {
            light: {
                primary: '#6366f1',
                primaryDark: '#4f46e5',
                accent: '#8b5cf6',
                textPrimary: '#0f172a',
                textSecondary: '#475569',
                bgLight: '#f8fafc',
                bgCard: '#ffffff',
                border: '#e2e8f0',
                success: '#22c55e',
                warning: '#f59e0b',
                error: '#ef4444'
            },
            dark: {
                primary: '#818cf8',
                primaryDark: '#6f71e5',
                accent: '#a78bfa',
                textPrimary: '#f1f5f9',
                textSecondary: '#94a3b8',
                bgLight: '#0f172a',
                bgCard: '#1e293b',
                border: '#334155',
                success: '#4ade80',
                warning: '#fbbf24',
                error: '#f87171'
            }
        },
        fonts: {
            display: ['Outfit', 'system-ui', 'sans-serif'],
            body: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['JetBrains Mono', 'Courier New', 'monospace']
        },
        spacing: {
            xs: '0.25rem',
            sm: '0.5rem',
            md: '1rem',
            lg: '1.5rem',
            xl: '2rem',
            '2xl': '3rem'
        }
    };

    function applyTokens(isDark) {
        const colors = isDark ? TOKENS.colors.dark : TOKENS.colors.light;
        const root = document.documentElement;
        
        root.style.setProperty('--color-primary', colors.primary);
        root.style.setProperty('--color-primary-dark', colors.primaryDark);
        root.style.setProperty('--color-accent', colors.accent);
        root.style.setProperty('--color-text-primary', colors.textPrimary);
        root.style.setProperty('--color-text-secondary', colors.textSecondary);
        root.style.setProperty('--color-bg-light', colors.bgLight);
        root.style.setProperty('--color-bg-card', colors.bgCard);
        root.style.setProperty('--color-border', colors.border);
        root.style.setProperty('--color-success', colors.success);
        root.style.setProperty('--color-warning', colors.warning);
        root.style.setProperty('--color-error', colors.error);
    }

    function getTheme() {
        return document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    }

    function setTheme(theme) {
        const root = document.documentElement;
        if (theme === 'dark') {
            root.classList.add('dark');
        } else {
            root.classList.remove('dark');
        }
        localStorage.setItem('ds-theme', theme);
        applyTokens(theme === 'dark');
    }

    function toggleTheme() {
        const current = getTheme();
        setTheme(current === 'dark' ? 'light' : 'dark');
    }

    function init() {
        const stored = localStorage.getItem('ds-theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = stored || (prefersDark ? 'dark' : 'light');
        
        setTheme(theme);
        return theme;
    }

    function getToken(name, type = 'colors') {
        const isDark = getTheme() === 'dark';
        const source = isDark ? TOKENS.dark : TOKENS.light;
        return TOKENS[type]?.[name] || null;
    }

    return {
        init,
        getTheme,
        setTheme,
        toggleTheme,
        applyTokens,
        getToken,
        TOKENS
    };
})();

if (typeof window !== 'undefined') {
    window.DesignTokens = DesignTokens;
}