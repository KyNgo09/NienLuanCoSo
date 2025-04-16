<template>
  <Header />
  <div class="container mx-auto p-4">
    <router-link to="/products" class="text-blue-500 text-lg hover:underline mb-6 inline-block">
      ← Quay lại danh sách sản phẩm
    </router-link>
    <div v-if="product" class="bg-white rounded-lg shadow-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <div class="grid grid-cols-2 gap-2">
            <img v-for="image in product.images" :key="image.id" :src="image.imageurl" alt="Hình ảnh sản phẩm"
              class="w-full h-40 object-cover rounded" @error="handleImageError" />
            <div v-if="!product.images || product.images.length === 0"
              class="col-span-2 h-40 bg-gray-200 flex items-center justify-center rounded">
              <span class="text-gray-500">Không có ảnh</span>
            </div>
          </div>
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ product.name }}</h1>
          <p class="text-customOrange font-bold text-xl mb-2">{{ formatPrice(product.price) }} VND</p>
          <p class="text-gray-700 mb-2"><strong>Danh mục:</strong> {{ getCategoryName(product.category) }}</p>
          <p class="text-gray-700 mb-4"><strong>Mô tả:</strong> {{ product.description }}</p>
          <div class="flex items-center mb-4">
            <button @click="decreaseQuantity" class="bg-customOrange text-white px-3 py-1 rounded-l hover:bg-orange-600"
              :disabled="quantity <= 1">-</button>
            <input type="number" v-model.number="quantity" min="1"
              class="w-14 text-center border-t border-b border-gray-200" readonly />
            <button @click="increaseQuantity"
              class="bg-customOrange text-white px-3 py-1 rounded-r hover:bg-orange-600">+</button>
          </div>
          <button @click="addToCart(product)"
            class="bg-customOrange text-white font-semibold px-4 py-2 rounded hover:bg-orange-600 transition flex items-center">
            <i class="fa fa-shopping-basket mr-2"></i> Thêm vào giỏ hàng
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-gray-500">Đang tải sản phẩm...</div>
    <!-- Sản phẩm khác -->
    <div v-if="relatedProducts.length" class="mt-8">
      <h2 class="text-4xl text-center font-sansita font-bold text-customBrown mb-4">Sản phẩm khác</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <router-link v-for="related in relatedProducts" :key="related.product_id"
          :to="{ name: 'ProductDetail', params: { id: related.product_id } }"
          class="border rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition">

          <img v-for="image in product.images" :key="image.id" :src="image.imageurl" alt="Hình ảnh sản phẩm"
            class="w-full h-40 object-cover rounded" @error="handleImageError" />

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
      quantity: 1
    };
  },
  methods: {
    async fetchProduct() {
      try {
        await this.fetchCategories();
        const response = await axios.get(`http://127.0.0.1:8000/api/products/${this.$route.params.id}/`);
        this.product = response.data;
        await this.fetchRelatedProducts();
      } catch (error) {
        console.error('Lỗi khi lấy chi tiết sản phẩm:', error);
        alert('Không thể tải sản phẩm.');
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = response.data;
        console.log('Dữ liệu danh mục:', this.categories);
      } catch (error) {
        console.error('Lỗi khi lấy danh mục:', error);
        this.categories = [];
      }
    },
    async fetchRelatedProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/products/');
        const products = response.data.filter(p => p.product_id !== parseInt(this.$route.params.id));
        this.relatedProducts = products.sort(() => Math.random() - 0.5).slice(0, 4);
        console.log('Sản phẩm liên quan:', this.relatedProducts);
      } catch (error) {
        console.error('Lỗi khi lấy sản phẩm khác:', error);
        this.relatedProducts = [];
      }
    },
    handleImageError(event) {
      console.error('Lỗi tải ảnh:', event.target.src, event);
      event.target.src = 'https://placehold.co/150x150?text=No+Image';
    },
    formatPrice(price) {
      if (!price && price !== 0) return '0';
      return parseInt(price).toLocaleString('vi-VN');
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(cat => cat.category_id === categoryId);
      return category ? category.name : 'Đang tải danh mục...';
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
          image: product.images && product.images.length > 0 ? product.images[0].imageurl : null,
          quantity: this.quantity
        });
      }
      localStorage.setItem('cart', JSON.stringify(cart));
      this.$root.$emit('cart-updated', cart.length); // Phát sự kiện
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
        this.fetchProduct();
      },
      immediate: true
    }
  }
};
</script>
