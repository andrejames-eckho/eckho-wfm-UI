/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'eckho-dark': '#333333',
        'eckho-light': '#D3D3D3',
      }
    },
  },
  plugins: [],
}
