
<template>
     <header class="w-full h-16 bg-white shadow-md flex items-center justify-between px-6">
    <!-- Logo -->
    <div class="flex items-center">
      <img src="@/assets/logo.png" alt="Logo" class="h-10">
    </div>

    <!-- Actions (Notifications & User Profile) -->
    <div class="flex items-center space-x-6">
      <!-- Chat Icon -->
      <font-awesome-icon :icon="['far', 'comment-dots']" class="text-gray-500 text-xl cursor-pointer hover:text-gray-700" />

      <!-- Notification Icon with Badge -->
      <div class="relative">
        <font-awesome-icon :icon="['far', 'bell']" class="text-gray-500 text-xl cursor-pointer hover:text-gray-700" />
        <span class="absolute top-0 right-0 bg-customOrange text-white text-xs font-bold rounded-full w-4 h-4 flex items-center justify-center">1</span>
      </div>

      <!-- User Profile -->
      <div class="flex items-center space-x-2 bg-gray-100 p-2 rounded-lg">
        <img src="" alt="User Avatar" class="h-8 w-8 rounded-full">
        <div>
          <p class="text-sm font-medium text-gray-700">Administrator</p>
          <p class="text-xs text-gray-500">ID: 1234567</p>
        </div>
      </div>
    </div>
  </header>
  </template>
  
  <script>
  export default {
    name: "Header",
  };
  </script>
  
  <style scoped>
  </style>
  