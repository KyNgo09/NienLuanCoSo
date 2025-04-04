<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="p-4">
        <h2 class="text-xl font-bold mb-2 text-gray-900 font-opensans">Danh mục sản phẩm</h2>
        <form @submit.prevent="createCategory" class="mb-4">
          <input v-model="newCategory" placeholder="Tên danh mục" class="border p-2 mr-2 text-black" />
          <button type="submit" class="bg-customOrange text-white p-2 font-bold font-opensans rounded-lg ">Thêm</button>
        </form>

        <table class="w-full border-collapse border border-gray -300 rounded-lg overflow-hidden">
          <thead>
            <tr class="bg-customOrange text-white text-left font-opensans">
              <th class="px-4 py-2">#</th>
              <th class="px-4 py-2">Tên danh mục</th>
              <th class="px-4 py-2">Thao tác</th>
            </tr>
          </thead>
          <tbody class="text-gray-700">
            <tr v-for="(cat, index) in categories" :key="cat.id" class="even:bg-gray-100 hover:bg-gray-200 transition">
              <td class="px-4 py-2">{{ index + 1 }}</td>
              <td class="px-4 py-2">{{ cat.name }}</td>
              <td class="px-4 py-2">
                <button @click="deleteCategory(cat.category_id)" class="text-red-500 hover:text-red-700 font-semibold">
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
      categories: [],
      newCategory: '',
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = res.data;
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
        this.categories = this.categories.filter(cat => cat.category_id !== id);
        alert("Xóa danh mục thành công!");
      } catch (error) {
        console.error("Lỗi khi xóa danh mục:", error);
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
