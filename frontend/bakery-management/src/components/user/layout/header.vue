<template>
  <header class="bg-white text-black shadow-md">
    <div class="container mx-auto flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center">
        <img src="@/assets/logo.png" alt="Logo" class="h-20 w-20 mr-2" />
      </div>

      <!-- Menu điều hướng -->
      <nav class="flex items-center space-x-6 flex-1">
        <!-- Trang chủ -->
        <router-link to="/" class="hover:text-customBrown">Trang chủ</router-link>

        <!-- Sản phẩm (Combobox) -->
        <div class="relative group">
          <button class="hover:text-customBrown flex items-center">
            Sản phẩm
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <!-- Dropdown -->
          <div class="absolute hidden group-hover:block bg-white text-black rounded-md shadow-lg mt-2 w-48 z-10">
            <router-link v-for="item in productItems" :key="item.path" :to="item.path"
              class="block px-4 py-2">
              {{ item.name }}
            </router-link>
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
          <span v-if="cartCount > 0" class="absolute top-0 right-0 -mt-2 -mr-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {{ cartCount }}
          </span>
        </router-link>
      </div>
    </div>
  </header>
</template>
  
  <script>
  export default {
    name: 'Header',
    data() {
      return {
        // Danh sách sản phẩm con trong combobox
        productItems: [
          { name: 'Điện thoại', path: '/products/phones' },
          { name: 'Máy tính', path: '/products/laptops' },
          { name: 'Phụ kiện', path: '/products/accessories' },
        ],
        // Trạng thái đăng nhập (giả lập)
        isLoggedIn: false,
        userName: 'User',
        cartCount: 2, // Số lượng sản phẩm trong giỏ hàng (giả lập)
      };
    },
    methods: {
      logout() {
        this.isLoggedIn = false;
        this.$router.push('/login');
        alert('Đã đăng xuất!');
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