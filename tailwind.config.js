/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./pages/**/*.html",
        "./components/**/*.js",
        "./js/**/*.js"
    ],
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: {
                display: ['Crimson Text', 'Georgia', 'serif'],
                body: ['Segoe UI', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'Courier New', 'monospace']
            },
            colors: {
                primary: {
                    50: '#f0f4ff',
                    100: '#e0e9ff',
                    200: '#c7d7fe',
                    300: '#a4b9fd',
                    400: '#7c93fb',
                    500: '#6366f1',
                    600: '#4f46e5',
                    700: '#4338ca',
                    800: '#3730a3',
                    900: '#312e81',
                    950: '#1e1b4b',
                },
                accent: {
                    50: '#f5f3ff',
                    100: '#ede9fe',
                    200: '#ddd6fe',
                    300: '#c4b5fd',
                    400: '#a78bfa',
                    500: '#8b5cf6',
                    600: '#7c3aed',
                    700: '#6d28d9',
                    800: '#5b21b6',
                    900: '#4c1d95',
                },
                slate: {
                    50: '#f8fafc',
                    100: '#f1f5f9',
                    200: '#e2e8f0',
                    300: '#cbd5e1',
                    400: '#94a3b8',
                    500: '#64748b',
                    600: '#475569',
                    700: '#334155',
                    800: '#1e293b',
                    900: '#0f172a',
                    950: '#020617',
                }
            },
            spacing: {
                '128': '32rem',
                '144': '36rem',
            },
            animation: {
                'fade-in': 'fadeIn 0.6s ease-in-out',
                'slide-up': 'slideUp 0.7s ease-out',
                'slide-in-left': 'slideInLeft 0.6s ease-out',
                'glow': 'glow 3s ease-in-out infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
                slideInLeft: {
                    '0%': { transform: 'translateX(-20px)', opacity: '0' },
                    '100%': { transform: 'translateX(0)', opacity: '1' },
                },
                glow: {
                    '0%, 100%': { boxShadow: '0 0 5px rgba(99, 102, 241, 0.5)' },
                    '50%': { boxShadow: '0 0 20px rgba(99, 102, 241, 0.8)' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            },
            backdropBlur: {
                xs: '2px',
            },
            boxShadow: {
                'glow': '0 0 20px rgba(99, 102, 241, 0.3)',
                'glow-lg': '0 0 40px rgba(99, 102, 241, 0.4)',
            }
        }
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
    ]
}
