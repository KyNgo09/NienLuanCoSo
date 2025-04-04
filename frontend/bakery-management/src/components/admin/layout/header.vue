<template>
  <div class="bg-white p-4 shadow-md flex justify-between items-center">
    <!-- Logo -->
    <div class="flex items-center space-x-2">
      <img src="@/assets/logo.png" alt="Logo" class="h-12" />
      <span class="text-xl font-semibold text-gray-700">Panadería</span>
    </div>

    <!-- User Actions -->
    <div class="flex items-center space-x-6">
      <button class="relative">
        <font-awesome-icon :icon="['far', 'comment-dots']" class="text-gray-500 text-xl" />
      </button>

      <button class="relative">
        <font-awesome-icon :icon="['far', 'bell']" class="text-gray-500 text-xl" />
        <span class="absolute -top-1 -right-1 bg-customOrange text-white text-xs w-4 h-4 flex items-center justify-center rounded-full">1</span>
      </button>

      <!-- User Info -->
      <div class="flex items-center space-x-2 cursor-pointer">
        <img src="" alt="User" class="w-10 h-10 rounded-full border" />
        <div>
          <p class="text-gray-700 font-medium">Administrator</p>
          <p class="text-gray-500 text-sm">ID: 1234567</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
};
</script>
