<template>
    <Header />
    <div class="container mx-auto p-4">
      <router-link to="/" class="text-blue-500 hover:underline mb-4 inline-block">
        ← Quay lại danh sách sản phẩm
      </router-link>
      <div v-if="product" class="bg-white rounded-lg shadow-lg p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div class="grid grid-cols-2 gap-2">
              <img
                v-for="image in product.images"
                :key="image.id"
                :src="image.imageurl"
                alt="Hình ảnh sản phẩm"
                class="w-full h-40 object-cover rounded"
                @error="handleImageError"
              />
              <div
                v-if="!product.images || product.images.length === 0"
                class="col-span-2 h-40 bg-gray-200 flex items-center justify-center rounded"
              >
                <span class="text-gray-500">Không có ảnh</span>
              </div>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ product.name }}</h1>
            <p class="text-customOrange font-bold text-xl mb-2">{{ formatPrice(product.price) }} VND</p>
            <p class="text-gray-700 mb-2"><strong>Danh mục:</strong> {{ getCategoryName(product.category) }}</p>
            <p class="text-gray-700 mb-2"><strong>Mô tả:</strong> {{ product.description }}</p>
          </div>
        </div>
      </div>
      <div v-else class="text-center text-gray-500">Đang tải sản phẩm...</div>
    </div>
    <Footer />
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
    name: 'ProductDetail',
    data() {
      return {
        product: null,
        categories: []
      };
    },
    methods: {
      async fetchProduct() {
        try {
          const response = await axios.get(`http://127.0.0.1:8000/api/products/${this.$route.params.id}/`);
          this.product = response.data;
        } catch (error) {
          console.error('Lỗi khi lấy chi tiết sản phẩm:', error);
          alert('Không thể tải sản phẩm.');
        }
      },
      async fetchCategories() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/categories/');
          this.categories = response.data;
        } catch (error) {
          console.error('Lỗi khi lấy danh mục:', error);
        }
      },
      handleImageError(event) {
        console.error('Lỗi tải ảnh:', event.target.src);
        event.target.src = 'https://placehold.co/150x150?text=No+Image';
      },
      formatPrice(price) {
        if (!price && price !== 0) return '0';
        return parseInt(price).toLocaleString('vi-VN');
      },
      getCategoryName(categoryId) {
        const category = this.categories.find(cat => cat.category_id === categoryId);
        return category ? category.name : 'Không xác định';
      }
    },
    mounted() {
      this.fetchProduct();
      this.fetchCategories();
    }
  };
  </script>