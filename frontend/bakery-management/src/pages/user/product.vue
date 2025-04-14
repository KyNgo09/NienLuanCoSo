<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    <h1 class="text-2xl font-bold mb-6 text-gray-900">Tất cả sản phẩm</h1>
    <div v-if="products.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <router-link
        v-for="product in products"
        :key="product.product_id"
        :to="{ name: 'ProductDetail', params: { id: product.product_id } }"
        class="border rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition"
      >
        <img
          v-if="product.images && product.images.length > 0"
          :src="product.images[0].imageurl"
          alt="Hình ảnh sản phẩm"
          class="w-full h-48 object-cover"
          @error="handleImageError($event, product.product_id)"
        />
        <div v-else class="w-full h-48 bg-gray-200 flex items-center justify-center">
          <span class="text-gray-500">Không có ảnh</span>
        </div>
        <div class="p-4">
          <h2 class="text-lg font-semibold text-gray-900">{{ product.name }}</h2>
          <p class="text-customOrange font-bold">{{ formatPrice(product.price) }} VND</p>
        </div>
      </router-link>
    </div>
    <div v-else class="text-center text-gray-500">
      Không có sản phẩm nào để hiển thị.
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
  name: 'Products',
  data() {
    return {
      products: []
    };
  },
  methods: {
    async fetchProducts() {
      try {
        console.log('Đang lấy danh sách sản phẩm...');
        const response = await axios.get('http://127.0.0.1:8000/api/products/', {
          timeout: 10000
        });
        console.log('Dữ liệu sản phẩm nhận được:', response.data);
        this.products = response.data;
        if (response.data.length === 0) {
          console.warn('Không có sản phẩm nào từ API.');
        }
      } catch (error) {
        console.error('Lỗi khi lấy sản phẩm:', error.response || error.message);
        alert('Không thể tải danh sách sản phẩm. Vui lòng thử lại sau.');
      }
    },
    handleImageError(event, productId) {
      console.error(`Lỗi tải ảnh cho sản phẩm ID ${productId}:`, event.target.src);
      event.target.src = 'https://placehold.co/150x150?text=No+Image';
    },
    formatPrice(price) {
      if (!price && price !== 0) return '0';
      return parseInt(price).toLocaleString('vi-VN');
    }
  },
  mounted() {
    this.fetchProducts();
  }
}
  </script>
  <style scoped>
  .router-link-active {
    text-decoration: none;
  }
  </style>