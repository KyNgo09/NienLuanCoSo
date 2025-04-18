<template>
  <Header />
  <div class="container mx-auto p-4">
    <router-link to="/products" class="text-blue-500 text-lg hover:underline mb-6 inline-block">
      ← Quay lại danh sách sản phẩm
    </router-link>
    <div v-if="product" class="bg-white rounded-lg shadow-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <!-- Hiển thị ảnh chính -->
          <div class="relative">
            <img v-if="product.images && product.images.length > 0" :src="product.images[currentImageIndex].imageurl"
              :alt="`Hình ảnh ${product.name}`" class="w-full h-64 object-cover rounded" loading="lazy"
              @error="handleImageError($event)" />
            <div v-else class="w-full h-64 bg-gray-200 flex items-center justify-center rounded">
              <span class="text-gray-500">Không có ảnh</span>
            </div>
            <!-- Nút chuyển ảnh -->
            <button v-if="product.images && product.images.length > 1" @click="prevImage"
              class="absolute left-2 top-1/2 transform -translate-y-1/2 bg-gray-200 p-2 rounded-full hover:bg-gray-300">
              < </button>
                <button v-if="product.images && product.images.length > 1" @click="nextImage"
                  class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gray-200 p-2 rounded-full hover:bg-gray-300">
                  >
                </button>
          </div>
          <!-- Danh sách ảnh thu nhỏ -->
          <div v-if="product.images && product.images.length > 1" class="grid grid-cols-4 gap-2 mt-2">
            <img v-for="(image, index) in product.images" :key="image.imageurl" :src="image.imageurl"
              :alt="`Ảnh thu nhỏ ${product.name}`" class="w-full h-16 object-cover rounded cursor-pointer"
              :class="{ 'border-2 border-customOrange': index === currentImageIndex }" loading="lazy"
              @click="currentImageIndex = index" @error="handleImageError($event)" />
          </div>
        </div>
        <div class="p-6 ">
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>
          <p class="text-xl font-semibold text-orange-500 mb-4">{{ formatPrice(product.price) }} VND</p>
          <p class="text-lg text-gray-700 mb-2">
            <span class="font-semibold">Danh mục:</span> {{ getCategoryName(product.category) }}
          </p>
          <p class="text-lg text-gray-700 mb-6">
            <span class="font-semibold">Mô tả:</span> {{ product.description }}
          </p>
          <div class="flex items-center space-x-2 mb-6">
            <button @click="decreaseQuantity"
              class="px-3 py-1 bg-orange-500 text-white rounded-l hover:bg-orange-600 disabled:bg-orange-300"
              :disabled="quantity <= 1">-</button>
            <input type="number" v-model.number="quantity" min="1"
              class="w-14 text-center border border-gray-300 rounded" readonly />
            <button @click="increaseQuantity"
              class="px-3 py-1 bg-orange-500 text-white rounded-r hover:bg-orange-600">+</button>
          </div>
          <div>
            <button v-if="product.stock_quantity > 0" @click="addToCart(product)"
              class="px-4 py-2 text-white font-semibold bg-orange-500 rounded hover:bg-orange-600 transition flex items-center justify-center space-x-2">
              <i class="fa fa-shopping-basket"></i>
              <span>Thêm vào giỏ hàng</span>
            </button>
            <button v-else disabled
              class=" px-4 py-2 text-white font-semibold bg-gray-400 rounded flex items-center justify-center space-x-2 cursor-not-allowed">
              <i class="fa fa-ban"></i>
              <span>Đã hết hàng</span>
            </button>
          </div>
        </div>

      </div>
    </div>
    <div v-else class="text-center text-gray-500">Đang tải sản phẩm...</div>
    <!-- Sản phẩm khác -->
    <div v-if="relatedProducts.length" class="mt-8">
      <h2 class="text-4xl text-center font-sansita font-bold text-customBrown mb-8">Sản phẩm khác</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <router-link v-for="related in relatedProducts" :key="related.product_id"
          :to="{ name: 'ProductDetail', params: { id: related.product_id } }"
          class="border rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition">
          <img v-if="related.images && related.images.length > 0" :src="related.images[0].imageurl"
            :alt="`Hình ảnh ${related.name}`" class="w-full h-40 object-cover rounded" loading="lazy"
            @error="handleImageError($event)" />
          <div v-else class="w-full h-40 bg-gray-200 flex items-center justify-center rounded">
            <span class="text-gray-500">Không có ảnh</span>
          </div>
          <div class="p-4">
            <h3 class="text-lg font-semibold text-gray-900">{{ related.name }}</h3>
            <p class="text-customOrange font-bold">{{ formatPrice(related.price) }} VND</p>
          </div>
        </router-link>
      </div>
    </div>
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
      categories: [],
      relatedProducts: [],
      quantity: 1,
      currentImageIndex: 0
    };
  },
  methods: {
    async fetchProduct() {
      try {
        await this.fetchCategories();
        const productResponse = await axios.get(
          `${import.meta.env.VITE_API_URL}/api/products/${this.$route.params.id}/`,
          { timeout: 10000 }
        );
        this.product = productResponse.data;
        await this.fetchRelatedProducts();
      } catch (error) {
        console.error('Lỗi khi lấy chi tiết sản phẩm:', error);
        alert('Không thể tải sản phẩm.');
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/categories/`, { timeout: 5000 });
        this.categories = response.data;
        console.log('Dữ liệu danh mục:', this.categories);
      } catch (error) {
        console.error('Lỗi khi lấy danh mục:', error);
        this.categories = [];
      }
    },
    async fetchRelatedProducts() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/products/`, { timeout: 10000 });
        this.relatedProducts = response.data
          .filter(p => p.product_id !== parseInt(this.$route.params.id))
          .sort(() => Math.random() - 0.5)
          .slice(0, 4);
        console.log('Sản phẩm liên quan:', this.relatedProducts);
      } catch (error) {
        console.error('Lỗi khi lấy sản phẩm khác:', error);
        this.relatedProducts = [];
      }
    },
    prevImage() {
      if (this.currentImageIndex > 0) {
        this.currentImageIndex--;
      } else {
        this.currentImageIndex = this.product.images.length - 1;
      }
    },
    nextImage() {
      if (this.currentImageIndex < this.product.images.length - 1) {
        this.currentImageIndex++;
      } else {
        this.currentImageIndex = 0;
      }
    },
    handleImageError(event) {
      console.error('Lỗi tải ảnh:', event.target.src);
      event.target.src = '/images/no-image.png';
    },
    formatPrice(price) {
      if (!price && price !== 0) return '0';
      return Number(price).toLocaleString('vi-VN', { minimumFractionDigits: 0 });
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(cat => cat.category_id === categoryId);
      return category ? category.name : 'Không xác định';
    },
    addToCart(product) {
      let cart = JSON.parse(localStorage.getItem('cart')) || [];
      const existingItem = cart.find(item => item.product_id === product.product_id);
      if (existingItem) {
        existingItem.quantity += this.quantity;
      } else {
        cart.push({
          product_id: product.product_id,
          name: product.name,
          price: product.price,
          image: product.images && product.images.length > 0 ? product.images[0].imageurl : '/images/no-image.png',
          quantity: this.quantity
        });
      }
      localStorage.setItem('cart', JSON.stringify(cart));
      this.$root.$emit('cart-updated', cart.length);
      alert(`${product.name} (x${this.quantity}) đã được thêm vào giỏ hàng!`);
      console.log('Giỏ hàng:', cart);
      this.quantity = 1;
    },
    increaseQuantity() {
      this.quantity++;
    },
    decreaseQuantity() {
      if (this.quantity > 1) {
        this.quantity--;
      }
    }
  },
  watch: {
    '$route.params.id': {
      handler(newId) {
        this.product = null;
        this.relatedProducts = [];
        this.quantity = 1;
        this.currentImageIndex = 0;
        this.fetchProduct();
      },
      immediate: true
    }
  }
};
</script>