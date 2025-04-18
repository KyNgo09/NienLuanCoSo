<template>
  <div class="flex flex-col min-h-screen w-full ">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="p-4 flex-1">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Thêm sản phẩm</h2>

        <!-- Form thêm sản phẩm -->
        <form @submit.prevent="createProduct" class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 mb-6 border rounded">
          <input v-model="newProduct.name" placeholder="Tên sản phẩm" class="border p-2 text-black rounded" />
          <select v-model="newProduct.category" class="w-full border p-2 rounded text-black">
            <option value="">-- Chọn danh mục --</option>
            <option v-for="category in categories" :key="category.category_id" :value="category.category_id">
              {{ category.name }}
            </option>
          </select>
          <textarea v-model="newProduct.description" placeholder="Mô tả"
            class="border p-2 text-black rounded md:col-span-2"></textarea>
          <input v-model.number="newProduct.price" type="number" step="0.01" placeholder="Giá"
            class="border p-2 text-black rounded" />
          <input v-model.number="newProduct.stock_quantity" type="number" placeholder="Số lượng"
            class="border p-2 text-black rounded" />
          <div>
            <label class="font-semibold text-gray-700">Ảnh sản phẩm:</label>
            <input type="file" accept="image/*" multiple @change="handleImageChange"
              class="border p-2 rounded w-full focus:outline-none focus:ring-2 focus:ring-customOrange" />
            <div v-if="selectedImages.length" class="flex flex-col space-y-2 mt-2">
              <div v-for="(image, index) in selectedImages" :key="index" class="flex items-center space-x-2">
                <span class="text-gray-700">{{ image.name }}</span>
                <button type="button" @click="removeImage(index)" class="text-red-500 hover:text-red-700 font-semibold">
                  Xóa
                </button>
              </div>
            </div>
          </div>
          <div class="md:col-span-2">
            <button type="submit" :disabled="isLoading" class="bg-customOrange text-white px-4 py-2 rounded font-bold">
              {{ isLoading ? 'Đang xử lý...' : 'Thêm sản phẩm' }}
            </button>
            <div v-if="isLoading" class="mt-2 flex items-center text-gray-700">
              <svg class="animate-spin h-5 w-5 mr-2 text-customOrange" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              Đang upload sản phẩm và ảnh...
            </div>
          </div>
        </form>

        <!-- Modal sửa sản phẩm -->
        <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-lg">
            <h3 class="text-lg font-bold mb-4 text-gray-900">Sửa sản phẩm</h3>
            <form @submit.prevent="updateProduct">
              <div class="grid grid-cols-1 gap-4">
                <label>
                  Tên sản phẩm
                  <input v-model="editProduct.name" placeholder="Tên sản phẩm"
                    class="w-full border p-2 rounded text-black" />
                </label>
                <label> Danh mục
                  <select v-model="editProduct.category" class="w-full border p-2 rounded text-black">
                    <option value="">-- Chọn danh mục --</option>
                    <option v-for="category in categories" :key="category.category_id" :value="category.category_id">
                      {{ category.name }}
                    </option>
                  </select>
                </label>
                <label>Mô tả
                  <textarea v-model="editProduct.description" placeholder="Mô tả"
                    class="w-full border p-2 text-black rounded"></textarea>
                </label>
                <label>Giá
                  <input v-model.number="editProduct.price" type="number" step="0.01" placeholder="Giá"
                    class="w-full border p-2 text-black rounded" />
                </label>
                <label>Số lượng
                  <input v-model.number="editProduct.stock_quantity" type="number" placeholder="Số lượng"
                    class="w-full border p-2 text-black rounded" />
                </label>
              </div>
              <div class="mt-4 flex justify-end space-x-2">
                <button type="button" @click="closeEditModal"
                  class="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400">
                  Hủy
                </button>
                <button type="submit" :disabled="isLoading"
                  class="bg-customOrange text-white px-4 py-2 rounded font-bold">
                  {{ isLoading ? 'Đang xử lý...' : 'Lưu' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Danh sách sản phẩm -->
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-800">Danh Sách Sản Phẩm</h2>
          <div class="flex space-x-4">
            <!-- Filter by category -->
            <select v-model="selectedCategory" @change="filterProducts" 
              class="border p-2 rounded text-black focus:outline-none focus:ring-2 focus:ring-customOrange">
              <option value="">Tất cả danh mục</option>
              <option v-for="category in categories" :key="category.category_id" :value="category.category_id">
                {{ category.name }}
              </option>
            </select>
            
            <!-- Filter low stock -->
            <button @click="toggleLowStockFilter" 
              :class="{
                'bg-gray-200 hover:bg-gray-300': !showLowStockOnly,
                'bg-red-500 hover:bg-red-600 text-white': showLowStockOnly
              }" 
              class="px-4 py-2 rounded transition">
              Sản phẩm sắp hết
            </button>
          </div>
        </div>

        <table class="w-full border-collapse border border-gray-300 rounded overflow-hidden">
          <thead>
            <tr class="bg-customOrange text-white text-left">
              <th class="px-4 py-2 border">Tên</th>
              <th class="px-4 py-2 border">Danh mục</th>
              <th class="px-4 py-2 border">Mô tả</th>
              <th class="px-4 py-2 border">Giá</th>
              <th class="px-4 py-2 border">Số lượng</th>
              <th class="px-4 py-2 border">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in filteredProducts" :key="product.product_id" :class="{
              'bg-gray-100 hover:bg-gray-200 transition text-gray-900': true,
              'bg-red-500 hover:bg-red-600': product.stock_quantity < 5
            }">
              <td class="px-4 py-2 border">{{ product.name }}</td>
              <td class="px-4 py-2 border">{{ getCategoryName(product.category) }}</td>
              <td class="px-4 py-2 border max-w-xs overflow-hidden text-ellipsis whitespace-nowrap" :title="product.description">
  {{ product.description }}
</td>
              <td class="px-4 py-2 border">{{ formatPrice(product.price) }} VND</td>
              <td class="px-4 py-2 border" :class="{ '': product.stock_quantity < 5 }">
                {{ product.stock_quantity }}
              </td>
              <td class="px-4 py-2 border">
                <button @click="deleteProduct(product.product_id)"
                  class="text-red-700 hover:text-red-900 font-semibold">
                  Xóa
                </button>
                <button @click="openEditModal(product)" class="text-blue-700 hover:text-blue-900 ml-5 font-semibold">
                  Sửa
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import LeftSidebar from "@/components/admin/layout/left_sidebar.vue";
import Header from "@/components/admin/layout/header.vue";
import axios from 'axios';

export default {
  components: {
    Header,
    LeftSidebar,
  },
  data() {
    return {
      products: [],
      filteredProducts: [],
      newProduct: {
        name: '',
        description: '',
        price: null,
        category: '',
        stock_quantity: null
      },
      selectedImages: [],
      categories: [],
      isLoading: false,
      showEditModal: false,
      editProduct: {
        product_id: null,
        name: '',
        description: '',
        price: null,
        category: '',
        stock_quantity: null
      },
      // Filter variables
      selectedCategory: '',
      showLowStockOnly: false
    };
  },
  methods: {
    handleImageChange(event) {
      const files = Array.from(event.target.files);
      this.selectedImages = files;
    },
    removeImage(index) {
      this.selectedImages.splice(index, 1);
    },
    formatPrice(price) {
      if (!price && price !== 0) return '0';
      return parseInt(price).toLocaleString('vi-VN');
    },
    async fetchCategories() {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = res.data;
      } catch (error) {
        console.error("Lỗi khi lấy danh mục:", error);
        alert('Lỗi khi lấy danh mục: ' + error.message);
      }
    },
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/products/');
        this.products = response.data;
        this.filteredProducts = [...this.products]; // Initialize filtered products
      } catch (error) {
        console.error('Lỗi khi lấy sản phẩm:', error);
        alert('Lỗi khi lấy sản phẩm: ' + error.message);
      }
    },
    // Filter methods
    filterProducts() {
      this.filteredProducts = this.products.filter(product => {
        // Filter by category
        const categoryMatch = !this.selectedCategory || product.category == this.selectedCategory;
        
        // Filter by low stock
        const stockMatch = !this.showLowStockOnly || product.stock_quantity < 5;
        
        return categoryMatch && stockMatch;
      });
    },
    toggleLowStockFilter() {
      this.showLowStockOnly = !this.showLowStockOnly;
      this.filterProducts();
    },
    async createProduct() {
      if (
        !this.newProduct.name ||
        this.newProduct.price === null ||
        !this.newProduct.category ||
        this.newProduct.stock_quantity === null ||
        !this.newProduct.description
      ) {
        alert('Vui lòng điền đầy đủ thông tin (tên, giá, danh mục, số lượng, mô tả)!');
        return;
      }

      try {
        this.isLoading = true;

        const data = {
          name: this.newProduct.name,
          description: this.newProduct.description,
          price: this.newProduct.price,
          category: this.newProduct.category,
          stock_quantity: this.newProduct.stock_quantity
        };

        const response = await axios.post('http://127.0.0.1:8000/api/products/', data, {
          headers: { 'Content-Type': 'application/json' },
          timeout: 10000
        });

        const productId = response.data.product_id;

        if (this.selectedImages.length > 0) {
          for (const image of this.selectedImages) {
            const formData = new FormData();
            formData.append('image', image);

            await axios.post(`http://127.0.0.1:8000/api/products/${productId}/upload-image/`, formData, {
              headers: { 'Content-Type': 'multipart/form-data' },
              timeout: 60000
            });
          }
        }

        this.newProduct = {
          name: '',
          description: '',
          price: null,
          category: '',
          stock_quantity: null
        };
        this.selectedImages = [];
        await this.fetchProducts();
        alert('Thêm sản phẩm thành công!');
      } catch (error) {
        const errorMsg =
          error.response?.data?.error ||
          error.response?.data?.detail ||
          error.message;
        console.error('Lỗi chi tiết:', error.response?.data || error);
        alert(`Lỗi khi thêm sản phẩm: ${errorMsg}`);
      } finally {
        this.isLoading = false;
      }
    },
    async deleteProduct(productId) {
      if (confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) {
        try {
          await axios.delete(`http://127.0.0.1:8000/api/products/${productId}/`);
          await this.fetchProducts();
          alert('Xóa sản phẩm thành công!');
        } catch (error) {
          console.error('Lỗi khi xóa sản phẩm:', error);
          alert('Lỗi khi xóa sản phẩm: ' + error.message);
        }
      }
    },
    openEditModal(product) {
      this.editProduct = {
        product_id: product.product_id,
        name: product.name,
        description: product.description,
        price: product.price,
        category: product.category,
        stock_quantity: product.stock_quantity
      };
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
      this.editProduct = {
        product_id: null,
        name: '',
        description: '',
        price: null,
        category: '',
        stock_quantity: null
      };
    },
    async updateProduct() {
      if (
        !this.editProduct.name ||
        this.editProduct.price === null ||
        !this.editProduct.category ||
        this.editProduct.stock_quantity === null ||
        !this.editProduct.description
      ) {
        alert('Vui lòng điền đầy đủ thông tin (tên, giá, danh mục, số lượng, mô tả)!');
        return;
      }

      try {
        this.isLoading = true;

        const data = {
          name: this.editProduct.name,
          description: this.editProduct.description,
          price: this.editProduct.price,
          category: this.editProduct.category,
          stock_quantity: this.editProduct.stock_quantity
        };

        await axios.put(`http://127.0.0.1:8000/api/products/${this.editProduct.product_id}/`, data, {
          headers: { 'Content-Type': 'application/json' },
          timeout: 10000
        });

        this.closeEditModal();
        await this.fetchProducts();
        alert('Cập nhật sản phẩm thành công!');
      } catch (error) {
        const errorMsg =
          error.response?.data?.error ||
          error.response?.data?.detail ||
          error.message;
        console.error('Lỗi chi tiết:', error.response?.data || error);
        alert(`Lỗi khi cập nhật sản phẩm: ${errorMsg}`);
      } finally {
        this.isLoading = false;
      }
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(cat => cat.category_id === categoryId);
      return category ? category.name : "Không xác định";
    }
  },
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
  }
};
</script>