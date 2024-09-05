/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/static/js/**/*.js',    // Include all JavaScript files in app/static/js
    './app/components/**/*.html', // Include all HTML files in app/components
    './app/templates/**/*.html',  // Include all HTML files in app/templates
    './app/templates/**/*.js'     // Include all JavaScript files in app/templates
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    // ...
  ],
}

