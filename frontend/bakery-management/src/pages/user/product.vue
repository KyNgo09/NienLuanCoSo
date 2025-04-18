<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    <div class="container mx-auto p-4">
      <h1 class="text-4xl font-bold mb-4 text-customBrown font-sansita">Tất cả sản phẩm</h1>
      <div class="flex flex-col md:flex-row gap-6">
        <div class="w-60 bg-white">
          <h3 class="text-xl font-bold text-gray-800 border-b pb-2 mb-4">Lọc theo danh mục</h3>
          <div class="space-y-3">
            
            <label class="flex items-center cursor-pointer">
              <input type="radio" v-model="selectedCategory" :value="null" @change="filterByCategory"
                class="text-orange-500 " />
              <span class="ml-3 text-gray-800 hover:text-orange-500 transition">Tất cả</span>
            </label>
            
            <label v-for="category in categories" :key="category.category_id" class="flex items-center cursor-pointer">
              <input type="radio" v-model="selectedCategory" :value="category.category_id" @change="filterByCategory"
                class="text-orange-500 " />
              <span class="ml-3 text-gray-800 hover:text-orange-500 transition">{{ category.name }}</span>
            </label>
          </div>
        </div>

        <div class="flex-1">
          <div v-if="isLoading" class="text-center py-4 text-gray-500">
            Đang tải sản phẩm...
          </div>
          <div v-else-if="products.length > 0"
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <router-link v-for="product in products" :key="product.product_id"
              :to="{ name: 'ProductDetail', params: { id: product.product_id } }"
              class="border rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition">
              <img v-if="product.images && product.images.length > 0" :src="product.images[0].imageurl"
                :alt="`Hình ảnh ${product.name}`" class="w-full h-48 object-cover" loading="lazy"
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
      selectedCategory: null,
      isLoading: false
    };
  },
  methods: {
    async fetchProducts(categoryId = null) {
      this.isLoading = true;
      try {
        const url = categoryId !== null && categoryId !== undefined
          ? `${import.meta.env.VITE_API_URL}/api/products/?category=${categoryId}`
          : `${import.meta.env.VITE_API_URL}/api/products/`;
        const response = await axios.get(url, { timeout: 10000 });
        this.products = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error('Lỗi khi lấy sản phẩm:', error);
        this.products = [];
      } finally {
        this.isLoading = false;
      }
    },
    async fetchCategories() {
      this.isLoading = true;
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/categories/`, { timeout: 5000 });
        this.categories = response.data;
      } catch (error) {
        console.error('Lỗi khi lấy danh mục:', error);
      } finally {
        this.isLoading = false;
      }
    },
    handleImageError(event, productId) {
      console.error(`Lỗi tải ảnh cho sản phẩm ID ${productId}:`, event.target.src);
      event.target.src = '/images/no-image.png';
    },
    formatPrice(price) {
      if (!price && price !== 0) return '0';
      return Number(price).toLocaleString('vi-VN', { minimumFractionDigits: 0 });
    },
    filterByCategory() {
      this.fetchProducts(this.selectedCategory);
    }
  },
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
  }
};
</script>