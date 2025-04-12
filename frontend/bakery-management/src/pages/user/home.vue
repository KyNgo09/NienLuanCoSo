<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    <router-view class="flex-grow" />
    <div>Home</div>
    <Footer />
  </div>
</template>
  
  <script>
  import Header from "@/components/user/layout/header.vue";
import Footer from "@/components/user/layout/footer.vue";
  export default {
  components: {
    Header,
    Footer,
  },
}
  </script>
  