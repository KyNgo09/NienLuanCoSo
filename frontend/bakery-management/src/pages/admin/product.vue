<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="p-4 flex-1">
        <h2 class="text-xl font-bold mb-4 text-gray-900 font-opensans">Quản lý sản phẩm</h2>

        <form @submit.prevent="createProduct" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
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
          <p>Hình ảnh</p>
          <input type="file" @change="handleFileUpload" multiple accept="image/*"
            class="border p-2 text-black rounded md:col-span-2" />
          <div class="md:col-span-2">
            <button type="submit" class="bg-customOrange text-white px-4 py-2 rounded font-bold">
              Thêm sản phẩm
            </button>
          </div>
        </form>

        <table class="w-full border-collapse border border-gray-300 rounded overflow-hidden">
          <thead>
            <tr class="bg-customOrange text-white text-left">
              <th class="px-4 py-2">ID</th>
              <th class="px-4 py-2">Tên</th>
              <th class="px-4 py-2">Danh mục</th>
              <th class="px-4 py-2">Mô tả</th>
              <th class="px-4 py-2">Giá</th>
              <th class="px-4 py-2">Số lượng</th>
              <th class="px-4 py-2">Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in products" :key="product.product_id"
              class="even:bg-gray-100 hover:bg-gray-200 transition text-gray-900">
              <td class="px-4 py-2">{{ index + 1 }}</td>
              <td class="px-4 py-2">{{ product.name }}</td>
              <td class="px-4 py-2">{{ getCategoryName(product.category) }}</td>
              <td class="px-4 py-2">{{ product.description }}</td>
              <td class="px-4 py-2">{{ product.price }}</td>
              <td class="px-4 py-2">{{ product.stock_quantity }}</td>
              <td class="px-4 py-2">
                <button @click="deleteProduct(product.product_id)" class="text-red-500 hover:text-red-700 font-semibold">
                  Xóa
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
      newProduct: {
        name: '',
        description: '',
        price: null,
        category: '',
        stock_quantity: null
      },
      selectedFiles: [],
      categories: [],
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = res.data;
        console.log("Danh sách danh mục:", this.categories);
      } catch (error) {
        console.error("Lỗi khi lấy danh mục:", error);
      }
    },
    handleFileUpload(event) {
      this.selectedFiles = event.target.files;
    },
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/products/');
        this.products = response.data;
      } catch (error) {
        console.error('Lỗi khi lấy sản phẩm:', error);
      }
    },
    async createProduct() {
      for (let file of this.selectedFiles) {
    if (!file.type.startsWith('image/')) {
      alert('Vui lòng chỉ chọn các tệp ảnh (JPG, PNG, v.v.)!');
      return;
    }
  }
  if (!this.newProduct.name || 
      this.newProduct.price === null || 
      !this.newProduct.category || 
      this.newProduct.stock_quantity === null || 
      !this.newProduct.description) {
    alert('Vui lòng điền đầy đủ thông tin (tên, giá, danh mục, số lượng, mô tả)!');
    return;
  }

  if (this.selectedFiles.length === 0) {
    alert('Vui lòng chọn ít nhất một hình ảnh!');
    return;
  }

  const formData = new FormData();
  formData.append('name', this.newProduct.name);
  formData.append('description', this.newProduct.description);
  formData.append('price', this.newProduct.price);
  formData.append('category', this.newProduct.category);
  formData.append('stock_quantity', this.newProduct.stock_quantity);

  for (let i = 0; i < this.selectedFiles.length; i++) {
    console.log('File:', this.selectedFiles[i].name, this.selectedFiles[i].type, this.selectedFiles[i].size);
    formData.append('images', this.selectedFiles[i]);
  }

  for (let pair of formData.entries()) {
    console.log(pair[0] + ': ' + pair[1]);
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/products/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log('Response:', response.data);
    this.newProduct = { name: '', description: '', price: null, category: '', stock_quantity: null };
    this.selectedFiles = [];
    await this.fetchProducts();
    alert('Thêm sản phẩm thành công!');
  } catch (error) {
    console.error('Lỗi khi thêm sản phẩm:', error.response ? error.response.data : error.message);
    alert('Có lỗi xảy ra khi thêm sản phẩm: ' + JSON.stringify(error.response ? error.response.data : error.message));
    // Kiểm tra lại danh sách sản phẩm ngay cả khi có lỗi
    await this.fetchProducts();
    const newProduct = this.products.find(p => p.name === this.newProduct.name);
    if (newProduct) {
      alert('Sản phẩm đã được thêm thành công dù có lỗi giao diện!');
      this.newProduct = { name: '', description: '', price: null, category: '', stock_quantity: null };
      this.selectedFiles = [];
    }
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
        }
      }
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(cat => cat.category_id === categoryId);
      return category ? category.name : "Không xác định";
    },
  },
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
  }
};
</script>