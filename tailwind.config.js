/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}",
    './node_modules/flowbite/**/*.js',
  ],
  plugins: [require('@tailwindcss/forms'),
require('flowbite/plugin')],
};
