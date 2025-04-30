/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        primary: '#FFCDAB',
        secondary: '#FFA45C',
        accent: '#5D5D5A'
      }
    }
  },
  plugins: [
    require('tailwindcss-motion')
  ]
}

