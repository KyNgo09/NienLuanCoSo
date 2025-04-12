/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sansita: ["Sansita Swashed", "cursive"],
        opensans: ["Open Sans", "sans-serif"],
      },
      colors: {
        customOrange: "#F3A446", // Màu cam
        customBrown: "#814A22", // Màu nâu
        customPeach: "#FFE1BC", // Màu đào nhạt
        customBlack: "#1F1711", // Màu 
      },
    },
  },
  plugins: [],
}

