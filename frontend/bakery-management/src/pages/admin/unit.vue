<template>
    <div class="flex flex-col min-h-screen w-full">
      <Header />
      <div class="flex flex-1 w-full">
        <LeftSidebar />
        <div class="p-4">
          <h2 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-4">Đơn vị đo lường</h2>
          <form @submit.prevent="createUnit" class="mb-4">
            <input v-model="newUnit" placeholder="Tên đơn vị" class="border p-2 mr-2 text-black" />
            <button type="submit" class="bg-customOrange text-white p-2 font-bold font-opensans rounded">Thêm</button>
          </form>
  
          <table class="w-full border-collapse border border-gray -300 rounded-lg overflow-hidden">
            <thead>
              <tr class="bg-customOrange text-white text-left font-opensans">
                <th class="px-4 py-2 border">STT</th>
                <th class="px-4 py-2 border">Tên đơn vị</th>
                <th class="px-4 py-2 border">Thao tác</th>
              </tr>
            </thead>
            <tbody class="text-gray-700">
              <tr v-for="(unit, index) in units" :key="unit.id" class="even:bg-gray-100 hover:bg-gray-200 transition">
                <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
                <td class="px-4 py-2 border text-center">{{ unit.name }}</td>
                <td class="px-4 py-2 border text-center">
                  <button @click="deleteUnit(unit.unit_id)" class="text-red-500 hover:text-red-700 font-semibold">
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
      units: [],
      newUnit: '',
    };
  },
  methods: {
    async fetchUnits() {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/units/');
        this.units = res.data;
        console.log("Danh sách đơn vị đo lường:", this.units); // Debug
      } catch (error) {
        console.error("Lỗi khi lấy đơn vị đo lường:", error);
      }
    },
    async createUnit() {
      if (!this.newUnit.trim()) return;
      try {
        await axios.post('http://127.0.0.1:8000/api/units/', {
          name: this.newUnit,
        });
        this.newUnit = '';
        await this.fetchUnits(); // Cập nhật danh sách sau khi tạo
        alert("Thêm đơn vị đo lường thành công!")
      } catch (error) {
        console.error("Lỗi khi tạo đơn vị đo lường:", error);
      }
    },
    async deleteUnit(id) {
      console.log("ID được truyền vào:", id); // Debug giá trị id
      if (!id || id === undefined) {
        console.error("ID không hợp lệ:", id);
        return;
      }
      if (!confirm("Bạn có chắc muốn xóa đơn vị đo lường này?")) return;
      try {
        console.log("URL gọi API:", `http://127.0.0.1:8000/api/units/${id}/`); // Debug URL
        await axios.delete(`http://127.0.0.1:8000/api/units/${id}/`);
        this.units = this.units.filter( unit => unit.unit_id !== id);
        alert("Xóa đơn vị đo lường thành công!");
      } catch (error) {
        console.error("Lỗi khi xóa đơn vị đo lường:", error);
        if (error.response) {
          console.error("Phản hồi từ server:", error.response.data);
        }
      }
    },
  },
  mounted() {
    this.fetchUnits();
  },
};
</script>