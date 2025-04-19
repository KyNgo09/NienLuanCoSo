<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    <div class="container mx-auto p-4">
      <h1 class="text-4xl font-bold mb-4 text-customBrown font-sansita">Tất cả sản phẩm</h1>
      <div class="flex flex-col md:flex-row gap-6">
        <div class="w-60 bg-white">
          <h3 class="text-xl font-bold text-gray-800 mb-4">Lọc theo danh mục</h3>
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
          <div v-else-if="paginatedProducts.length > 0"
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <router-link v-for="product in paginatedProducts" :key="product.product_id"
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

          <!-- Pagination Controls -->
          <div v-if="products.length > itemsPerPage" class="flex justify-center mt-6 space-x-2">
            <button @click="prevPage" :disabled="currentPage === 1"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50">
              Trước
            </button>
            <button v-for="page in totalPages" :key="page" @click="goToPage(page)"
              :class="[
                'px-4 py-2 rounded',
                currentPage === page ? 'bg-customOrange text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              ]">
              {{ page }}
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 disabled:opacity-50">
              Sau
            </button>
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
      isLoading: false,
      currentPage: 1,
      itemsPerPage: 12 // 4 columns * 3 rows
    };
  },
  computed: {
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.products.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.products.length / this.itemsPerPage);
    }
  },
  methods: {
    async fetchProducts(categoryId = null) {
      this.isLoading = true;
      this.currentPage = 1; // Reset to first page when fetching new products
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
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    }
  },
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
  }
};
</script>