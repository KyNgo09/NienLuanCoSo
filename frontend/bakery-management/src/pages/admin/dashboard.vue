<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="flex-1 p-6">
        <h1 class="text-2xl font-bold">Dashboard</h1>
        <router-view />
      </div>
    </div>
  </div>
</template>


<script>
import LeftSidebar from "@/components/admin/layout/left_sidebar.vue";
import Header from "@/components/admin/layout/header.vue";

export default {
  components: {
    Header,
    LeftSidebar,
  },
};
</script>