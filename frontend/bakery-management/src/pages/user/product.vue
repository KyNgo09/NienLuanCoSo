<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    <div class="container mx-auto p-4">
      <h1 class="text-4xl font-bold mb-4 text-customBrown font-sansita">Tất cả sản phẩm</h1>
      <div class="flex flex-col md:flex-row gap-6">
        <div class="w-48">
          <h3 class="text-lg font-semibold text-gray-700 mb-2 ">Lọc theo danh mục</h3>
          <div class="space-y-2">
            <label class="flex items-center">
              <input type="radio" v-model="selectedCategory" :value="null" @change="filterByCategory"
                class="text-customOrange focus:ring-customOrange" />
              <span class="ml-2 text-gray-700">Tất cả</span>
            </label>
            <label v-for="category in categories" :key="category.category_id" class="flex items-center">
              <input type="radio" v-model="selectedCategory" :value="category.category_id" @change="filterByCategory"
                class="text-customOrange focus:ring-customOrange" />
              <span class="ml-2 text-gray-700">{{ category.name }}</span>
            </label>
          </div>
        </div>
        <div class="flex-1">
          <div v-if="products.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <router-link v-for="product in products" :key="product.product_id"
              :to="{ name: 'ProductDetail', params: { id: product.product_id } }"
              class="border rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition">
              <img v-if="product.images && product.images.length > 0" :src="product.images[0].imageurl"
                alt="Hình ảnh sản phẩm" class="w-full h-48 object-cover"
                @error="handleImageError($event, product.product_id)" />
              <div v-else class="w-full h-48 bg-gray-200 flex items-center justify-center">
                <span class="text-gray-500">Không có ảnh</span>
              </div>
              <div class="p-4">
                <h2 class="text-lg font-opensans font-bold text-gray-700">{{ product.name }}</h2>
                <p class="text-customOrange font-semibold text-right">{{ formatPrice(product.price) }} VND</p>
              </div>
            </router-link>
          </div>
          <div v-else class="text-center text-gray-500">
            Không có sản phẩm nào để hiển thị.
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>


<script>
import Header from "@/components/user/layout/header.vue";
import Footer from "@/components/user/layout/footer.vue";
import axios from 'axios';

export default {
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      products: [],
      categories: [],
      selectedCategory: null
    };
  },
  methods: {
    async fetchProducts(categoryId = null) {
      try {
        console.log('Đang lấy danh sách sản phẩm với categoryId:', categoryId);
        const url = categoryId !== null && categoryId !== undefined
          ? `http://127.0.0.1:8000/api/products/?category=${categoryId}`
          : 'http://127.0.0.1:8000/api/products/';
        console.log('Gửi request tới:', url);
        const response = await axios.get(url, {
          timeout: 10000
        });
        console.log('Dữ liệu sản phẩm nhận được:', response.data);
        this.products = Array.isArray(response.data) ? response.data : [];
        if (this.products.length === 0) {
          console.warn('Không có sản phẩm nào từ API.');
        }
      } catch (error) {
        console.error('Lỗi khi lấy sản phẩm:', error.response || error.message);
        this.products = [];
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/categories/');
        console.log('Dữ liệu danh mục nhận được:', response.data);
        this.categories = response.data;
      } catch (error) {
        console.error('Lỗi khi lấy danh mục:', error);
      }
    },
    handleImageError(event, productId) {
      console.error(`Lỗi tải ảnh cho sản phẩm ID ${productId}:`, event.target.src, event);
      event.target.src = 'https://placehold.co/150x150?text=No+Image';
    },
    formatPrice(price) {
      if (!price && price !== 0) return '0';
      return parseInt(price).toLocaleString('vi-VN');
    },
    filterByCategory() {
      console.log('Lọc với selectedCategory:', this.selectedCategory);
      this.fetchProducts(this.selectedCategory);
    }
  },
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
  }
}
</script>
