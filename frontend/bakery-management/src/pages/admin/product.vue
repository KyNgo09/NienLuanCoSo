<template>
    <div class="flex min-h-screen">
      <!-- Sidebar -->
      <LeftSidebar />
  
      <!-- Main content -->
      <div class="flex-1 p-6">
        <h1 class="text-2xl font-bold">Category</h1>
        <router-view />
      </div>
    </div>
  </template>
  
  <script>
  import LeftSidebar from "@/components/admin/layout/left_sidebar.vue"; 
  
  export default {
    components: {
      LeftSidebar,
    },
  };
  </script>
  