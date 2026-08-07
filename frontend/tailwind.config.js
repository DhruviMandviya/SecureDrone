/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'tactical-bg': '#0a0e14',
        'tactical-panel': '#0d1117',
        'tactical-border': '#2a3441',
        'tactical-gray': '#1e242c',
        'tactical-text': '#a8b0ba',
        'signal-cyan': '#00f0ff',
        'signal-green': '#00ff41',
        'alert-amber': '#ffb000',
        'alert-red': '#ff2a2a',
      },
      fontFamily: {
        'mono': ['"JetBrains Mono"', 'monospace'],
        'sans': ['"Inter"', 'sans-serif'],
        'display': ['"Space Mono"', 'monospace'],
      },
      borderRadius: {
        'sm': '2px',
        DEFAULT: '2px',
        'md': '2px',
        'lg': '2px',
        'xl': '2px',
        '2xl': '2px',
        '3xl': '2px'
      }
    },
  },
  plugins: [],
}
