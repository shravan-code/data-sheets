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
                sans: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
                mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
            },
            colors: {
                surface: '#0b141c',
                'surface-dim': '#0b141c',
                'surface-bright': '#313a43',
                'surface-container-lowest': '#060f16',
                'surface-container-low': '#141c24',
                'surface-container': '#182028',
                'surface-container-high': '#222b33',
                'surface-container-highest': '#2d363e',
                'on-surface': '#dae3ee',
                'on-surface-variant': '#c6c6cb',
                outline: '#8f9095',
                'outline-variant': '#45474b',
                primary: '#c3c6cf',
                'on-primary': '#2d3137',
                'secondary-fixed': '#5bffa1',
                'secondary-container': '#27ff97',
                'on-secondary': '#00391d',
                background: '#0b141c',
                'primary-container': '#0d1117',
            },
            animation: {
                'fade-in': 'fadeIn 0.3s ease-out',
                'slide-up': 'slideUp 0.4s ease-out',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(10px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
            },
        }
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
    ]
}
