<template>
  <header class="bg-white text-black shadow-md">
    <div class="container mx-auto flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center">
        <img src="@/assets/logo.png" alt="Logo" class="h-20 w-20 mr-2" />
      </router-link>
      <!-- Menu điều hướng -->
      <nav class="flex items-center space-x-6 flex-1">
        <!-- Trang chủ -->
        <router-link to="/" class="hover:text-customBrown">Trang chủ</router-link>

        <!-- Sản phẩm (Combobox) -->
        <div class="relative group">
          <router-link to="/products" class="hover:text-customBrown flex items-center">
            Sản phẩm
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </router-link>
          <!-- Dropdown -->
          <div
            class="absolute opacity-0 group-hover:opacity-100 bg-white text-black rounded-md shadow-lg mt-2 w-48 z-10">
            <router-link v-for="item in productItems" :key="item.path" :to="item.path"
              class="block px-4 py-2 hover:text-customBrown">
              {{ item.name }}
            </router-link>
            <div v-if="productItems.length === 0" class="px-4 py-2 text-gray-500">Không có danh mục</div>
          </div>
        </div>

        <!-- Giới thiệu -->
        <router-link to="/about" class="hover:text-customBrown">Giới thiệu</router-link>

        <!-- Liên hệ -->
        <router-link to="/contact" class="hover:text-customBrown">Liên hệ</router-link>
      </nav>

      <!-- Tài khoản & Giỏ hàng -->
      <div class="flex items-center space-x-6 font-opensans">
        <!-- Tài khoản (Biểu tượng User) -->
        <router-link to="/account" class="flex flex-col items-center hover:text-customBrown">
          <i class="far fa-user w-6 h-6 text-gray-700"></i>
          <span class="text-sm">Tài khoản</span>
        </router-link>

        <!-- Giỏ hàng -->
        <router-link to="/cart" class="flex flex-col items-center relative hover:text-customBrown">
          <i class="fa fa-shopping-basket w-6 h-6 text-gray-700 "></i>
          <span class="text-sm">Giỏ hàng</span>
          <span v-if="cartCount > 0"
            class="absolute top-0 right-0 -mt-2 -mr-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {{ cartCount }}
          </span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Header',
  data() {
    return {
      productItems: [],
      cartCount: 2,
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.productItems = response.data.map(category => ({
          name: category.name,
          path: `/products/${category.name}`,
        }));
        console.log('Danh mục đã tải:', this.productItems); 
      } catch (error) {
        console.error('Lỗi khi lấy danh mục:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Tùy chỉnh thêm nếu cần */
.group:hover .group-hover\:block {
  display: block;
}
</style>