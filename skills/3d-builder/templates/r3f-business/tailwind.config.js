/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#__BRAND_50__',
          100: '#__BRAND_100__',
          400: '#__BRAND_400__',
          500: '#__BRAND_500__',
          600: '#__BRAND_600__',
          900: '#__BRAND_900__',
        },
        ink: {
          50: '#fafafa',
          100: '#f5f5f5',
          800: '#1a1a1a',
          900: '#0a0a0a',
          950: '#050505',
        },
      },
      fontFamily: {
        display: ['__FONT_DISPLAY__', 'serif'],
        sans: ['__FONT_SANS__', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
