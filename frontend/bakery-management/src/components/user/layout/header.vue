<template>
  <header class="bg-white text-black font-normal shadow-md sticky top-0 z-50">
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
          </router-link>
        </div>

        <!-- Giới thiệu -->
        <router-link to="/about" class="hover:text-customBrown">Giới thiệu</router-link>

        <!-- Liên hệ -->
        <router-link to="/contact" class="hover:text-customBrown">Liên hệ</router-link>
      </nav>

      <!-- Tài khoản & Giỏ hàng -->
      <div class="flex items-center space-x-6 font-opensans">
        <!-- Tài khoản (Biểu tượng User) -->
        <div class="relative">
          <div class="flex flex-col items-center hover:text-customBrown cursor-pointer" @click="toggleDropdown">
            <i class="far fa-user w-6 h-6 text-gray-700"></i>
            <span class="text-sm">Tài khoản</span>
          </div>
          <!-- Dropdown -->
          <div v-if="showDropdown"
            class="absolute bg-white text-black rounded-md shadow-lg mt-2 w-64 z-10 top-full right-0" @click.stop>
            <div v-if="isLoggedIn" class="p-4">
              <div class="flex items-center space-x-4">
                <img src="@/assets/user.png" alt="Avatar" class="h-12 w-12 rounded-full object-cover" />
                <div>
                  <p class="font-semibold">Xin chào! {{ user?.username || 'User' }}</p>
                  <p class="text-sm text-gray-600">Điểm tích lũy: {{ customer?.loyalty_point || 0 }}</p>
                </div>
              </div>
              <button @click="logout"
                class="mt-4 w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition duration-200 text-sm">
                Đăng xuất
              </button>
              <router-link to="/recent_orders"
                class="mt-2 w-full font-semibold text-gray-800 py-2 rounded-lg hover:text-orange-500 transition duration-200 text-sm flex items-center justify-center">
                Lịch sử mua hàng
              </router-link>
            </div>
            <div v-else class="p-4 text-center">
              <p class="text-gray-500 mb-4">Chưa đăng nhập</p>
              <router-link to="/account"
                class="block w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200 text-sm">
                Đăng nhập
              </router-link>
            </div>
          </div>
        </div>

        <!-- Giỏ hàng -->
        <router-link to="/cart" class="flex flex-col items-center relative hover:text-customBrown">
          <i class="fa fa-shopping-basket w-6 h-6 text-gray-700"></i>
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
      cartCount: JSON.parse(localStorage.getItem('cart'))?.length || 0,
      user: JSON.parse(localStorage.getItem('user')) || null,
      customer: JSON.parse(localStorage.getItem('customer')) || null,
      isLoggedIn: !!localStorage.getItem('user_id'),
      showDropdown: false,
    };
  },
  created() {
    this.updateAuthState();
    this.updateCartCount();
    document.addEventListener('click', this.handleClickOutside);
    window.addEventListener('storage', this.handleStorageChange);

  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
    window.removeEventListener('storage', this.handleStorageChange);
  },
  watch: {
    '$route'() {
      this.updateAuthState();
      this.showDropdown = false;
    }
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
    updateAuthState() {
      const user = JSON.parse(localStorage.getItem('user')) || null;
      const customer = JSON.parse(localStorage.getItem('customer')) || null;
      const userId = localStorage.getItem('user_id');
      this.user = user;
      this.customer = customer;
      this.isLoggedIn = !!userId;
      console.log('Auth state updated:', {
        user,
        customer,
        userId,
        isLoggedIn: this.isLoggedIn,
      });
    },
    updateCartCount() {
      const cart = JSON.parse(localStorage.getItem('cart')) || [];
      this.cartCount = cart.length;
      console.log('Cart count updated:', this.cartCount);
    },
    handleStorageChange() {
      this.updateAuthState();
      this.updateCartCount();
    },
    logout() {
      localStorage.removeItem('user');
      localStorage.removeItem('customer');
      localStorage.removeItem('user_id');
      this.user = null;
      this.customer = null;
      this.isLoggedIn = false;
      this.showDropdown = false;
      window.location.reload();
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    handleClickOutside(event) {
      const dropdown = this.$el.querySelector('.absolute');
      if (dropdown && !dropdown.contains(event.target) && !this.$el.querySelector('.cursor-pointer').contains(event.target)) {
        this.showDropdown = false;
      }
    },
  },
};
</script>

<style scoped></style>