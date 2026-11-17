/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        finance: {
          navy: '#0F172A',
          primary: '#1E3A8A',
          secondary: '#3B82F6',
          accent: '#10B981',
          bg: '#F8FAFC',
          card: '#FFFFFF',
          border: '#E2E8F0',
          text: '#0F172A',
          muted: '#64748B'
        }
      }
    },
  },
  plugins: [],
}
