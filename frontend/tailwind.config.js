/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ayur: {
          dark: '#0c110e',
          card: '#141c16',
          border: '#233327',
          emerald: '#10b981',
          gold: '#f59e0b',
        }
      }
    },
  },
  plugins: [],
}
