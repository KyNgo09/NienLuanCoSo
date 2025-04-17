<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="flex-1 p-6 bg-gray-50">
        <h1 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-4">Báo cáo doanh thu</h1>
        <div>
          <h2 class="text-xl font-semibold mb-4 text-gray-700">Doanh thu theo tháng</h2>
          <div v-if="isLoading" class="text-center text-gray-500 italic animate-pulse">
            Đang tải dữ liệu...
          </div>
          <div v-else-if="monthlyRevenue.length" class="overflow-x-auto">
            <table class="min-w-full bg-white border rounded-lg shadow-md">
              <thead class="bg-customOrange text-white">
                <tr>
                  <th class="py-3 px-5 border">Tháng</th>
                  <th class="py-3 px-5 border">Doanh thu (VND)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="entry in monthlyRevenue" :key="entry.month"
                  :class="index % 2 === 0 ? 'bg-gray-100' : 'bg-white'" class="">
                  <td class="py-3 px-5 border text-center text-gray-800">{{ entry.month }}</td>
                  <td class="py-3 px-5 border text-center text-gray-800">{{ formatPrice(entry.revenue) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center text-gray-500 italic">
            Không có dữ liệu doanh thu.
          </div>
        </div>
        <router-view />
      </div>

    </div>
  </div>
</template>


<script>
import LeftSidebar from "@/components/admin/layout/left_sidebar.vue";
import Header from "@/components/admin/layout/header.vue";
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  components: {
    Header,
    LeftSidebar,
  },
  data() {
    return {
      orders: [],
      monthlyRevenue: [], 
      isLoading: false,
    };
  },
  async mounted() {
    await this.fetchOrders();
    this.processRevenueData();
  },
  methods: {
    async fetchOrders() {
      this.isLoading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/orders/');
        this.orders = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error('Lỗi khi lấy danh sách đơn hàng:', error);
        alert('Không thể tải dữ liệu doanh thu.');
      } finally {
        this.isLoading = false;
      }
    },
    processRevenueData() {
      const revenueMap = {};

      // Tổng hợp doanh thu theo tháng
      this.orders.forEach(order => {
        const date = new Date(order.order_date);
        const monthYear = `${date.getMonth() + 1}/${date.getFullYear()}`; // Ví dụ: "1/2025"
        const amount = parseFloat(order.final_amount) || 0;

        if (!revenueMap[monthYear]) {
          revenueMap[monthYear] = 0;
        }
        revenueMap[monthYear] += amount;
      });

      // Chuyển thành mảng và sắp xếp theo thời gian
      this.monthlyRevenue = Object.keys(revenueMap)
        .map(month => ({
          month,
          revenue: revenueMap[month],
        }))
        .sort((a, b) => {
          const [monthA, yearA] = a.month.split('/').map(Number);
          const [monthB, yearB] = b.month.split('/').map(Number);
          return yearA - yearB || monthA - monthB;
        });
    },
    formatPrice(price) {
      return parseFloat(price).toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
    },
  },
};
</script>