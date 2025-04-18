<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="p-4">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh mục sản phẩm</h2>
        <form @submit.prevent="createCategory" class="mb-4">
          <input v-model="newCategory" placeholder="Tên danh mục" class="border p-2 mr-2 text-black" />
          <button type="submit" class="bg-customOrange text-white p-2 font-bold font-opensans rounded">Thêm</button>
        </form>

        <table class="w-full border-collapse border border-gray -300 rounded-lg overflow-hidden">
          <thead>
            <tr class="bg-customOrange text-white text-left font-opensans">
              <th class="px-4 py-2 borde text-centerr">STT</th>
              <th class="px-4 py-2 borde text-centerr">Tên danh mục</th>
              <th class="px-4 py-2 border text-center">Thao tác</th>
            </tr>
          </thead>
          <tbody class="text-gray-700">
            <tr v-for="(cat, index) in categories" :key="cat.id" class="even:bg-gray-100 hover:bg-gray-200 transition">
              <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ cat.name }}</td>
              <td class="px-4 py-2 border text-center">
                <button @click="deleteCategory(cat.id)" class="text-red-500 hover:text-red-700 font-semibold">
                  Xóa
                </button>
                <button @click="editCategory(cat)" class="text-blue-500 hover:text-blue-700 ml-5">Sửa</button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- Form sửa (hiển thị khi nhấn nút Sửa) -->
        <div v-if="editingCategory" class="mt-4">
          <form @submit.prevent="updateCategory" class="grid grid-cols-1 gap-4">
            <input v-model="editingCategory.name" placeholder="Tên danh mục" class="border p-2 rounded" />
            <div class="flex space-x-2">
              <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded">Cập nhật</button>
              <button @click="editingCategory = null" class="bg-gray-500 text-white px-4 py-2 rounded">Hủy</button>
            </div>
          </form>
        </div>
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
      categories: [],
      newCategory: '',
      editingCategory: null,
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = res.data.map(cat => ({
          id: cat.id || cat.category_id, // Chuẩn hóa id
          name: cat.name,
        }));
        console.log("Danh sách danh mục:", this.categories); // Debug
      } catch (error) {
        console.error("Lỗi khi lấy danh mục:", error);
      }
    },
    async createCategory() {
      if (!this.newCategory.trim()) return;
      try {
        await axios.post('http://127.0.0.1:8000/api/categories/', {
          name: this.newCategory,
        });
        this.newCategory = '';
        await this.fetchCategories(); // Cập nhật danh sách sau khi tạo
        alert("Thêm danh mục thành công!")
      } catch (error) {
        console.error("Lỗi khi tạo danh mục:", error);
      }
    },
    async deleteCategory(id) {
      console.log("ID được truyền vào:", id); // Debug giá trị id
      if (!id || id === undefined) {
        console.error("ID không hợp lệ:", id);
        return;
      }
      if (!confirm("Bạn có chắc muốn xóa danh mục này?")) return;
      try {
        console.log("URL gọi API:", `http://127.0.0.1:8000/api/categories/${id}/`); // Debug URL
        await axios.delete(`http://127.0.0.1:8000/api/categories/${id}/`);
        this.categories = this.categories.filter(cat => cat.id !== id);
        alert("Xóa danh mục thành công!");
      } catch (error) {
        console.error("Lỗi khi xóa danh mục:", error);
        if (error.response) {
          console.error("Phản hồi từ server:", error.response.data);
        }
      }
    },
    editCategory(category) {
      this.editingCategory = {
        id: category.id || category.category_id, // Đảm bảo lấy đúng id
        name: category.name,
      };
    },
    async updateCategory() {
      if (!this.editingCategory || !this.editingCategory.name.trim()) return;
      const categoryId = this.editingCategory.id;      
      try {
        await axios.put(`http://127.0.0.1:8000/api/categories/${categoryId}/`, {
          name: this.editingCategory.name,
        });
        this.editingCategory = null; // Ẩn form sau khi cập nhật
        await this.fetchCategories(); // Cập nhật danh sách
        alert("Cập nhật danh mục thành công!");
      } catch (error) {
        console.error("Lỗi khi cập nhật danh mục:", error);
        if (error.response) {
          console.error("Phản hồi từ server:", error.response.data);
        }
      }
    },
  },
  mounted() {
    this.fetchCategories();
  },
};
</script>
