<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="flex-1 p-6 ">
        <h1 class="text-2xl font-bold mb-6 text-gray-800">Báo cáo doanh thu</h1>
        <div>
          <h2 class="text-xl font-semibold mb-4 text-gray-700">Doanh thu theo tháng</h2>
          <div v-if="isLoading" class="text-center text-gray-500 italic animate-pulse">
            Đang tải dữ liệu...
          </div>
          <div v-else-if="monthlyRevenue.length" class="mt-6">
            <canvas id="revenueChart" class="max-w-full"></canvas>
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
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

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
      chart: null,
    };
  },
  async mounted() {
    await this.fetchOrders();
    this.processRevenueData();
    this.renderChart();
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
        const monthYear = `${date.getMonth() + 1}/${date.getFullYear()}`;
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
    renderChart() {
      if (!this.monthlyRevenue.length) return;

      const ctx = document.getElementById('revenueChart').getContext('2d');

      // Nếu biểu đồ đã tồn tại, hủy nó trước khi tạo mới
      if (this.chart) {
        this.chart.destroy();
      }

      // Tạo biểu đồ mới
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.monthlyRevenue.map(entry => entry.month),
          datasets: [{
            label: 'Doanh thu (VND)',
            data: this.monthlyRevenue.map(entry => entry.revenue),
            backgroundColor: '#FFE1BC', // Màu nền cột
            borderColor: '#FFE1BC', // Màu viền cột
            borderWidth: 1,
          }],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function (value) {
                  return value.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
                },
              },
            },
          },
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  let label = context.dataset.label || '';
                  if (label) {
                    label += ': ';
                  }
                  if (context.parsed.y !== null) {
                    label += context.parsed.y.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
                  }
                  return label;
                },
              },
            },
          },
        },
      });
    },
  },
  watch: {
    // Theo dõi thay đổi của monthlyRevenue để cập nhật biểu đồ
    monthlyRevenue: {
      handler() {
        this.$nextTick(() => {
          this.renderChart();
        });
      },
      deep: true,
    },
  },
};
</script>