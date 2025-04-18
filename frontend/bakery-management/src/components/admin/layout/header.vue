<template>
  <div class="bg-white p-4 shadow-md flex justify-between items-center sticky top-0 z-50">
    <!-- Logo -->
    <div class="flex items-center space-x-2">
      <img src="@/assets/logo.png" alt="Logo" class="h-12" />
      <span class="text-xl font-semibold text-gray-700">Panadería</span>
    </div>

    <!-- User Actions -->
    <div class="flex items-center space-x-6">
      <!-- Notifications -->
      <div class="relative">
        <button @click="toggleNotifications" class="relative focus:outline-none">
          <font-awesome-icon :icon="['far', 'bell']" class="text-gray-500 text-xl" />
          <span v-if="hasUnprocessedOrders" class="absolute -top-1 -right-1 bg-customOrange text-white text-xs w-4 h-4 flex items-center justify-center rounded-full">
            {{ unprocessedOrdersCount }}
          </span>
        </button>
        
        <!-- Notifications Dropdown -->
        <div v-if="showNotifications" class="absolute right-0 mt-2 w-80 bg-white border rounded-lg shadow-lg z-50">
          <div class="p-4">
            <h3 class="text-lg font-semibold text-gray-700">Đơn hàng mới</h3>
            <div v-if="hasUnprocessedOrders" class="mt-2">
              <div v-for="order in displayedOrders" :key="order.order_id" class="py-2 border-b last:border-b-0">
                <router-link 
                  :to="{ name: 'order', query: { orderId: order.order_id } }" 
                  @click="closeNotifications"
                  class="block hover:bg-gray-100 p-2 rounded"
                >
                  <p class="text-sm font-medium text-gray-800">
                    Đơn #{{ order.order_id }} - {{ order.customer?.name || 'Khách vãng lai' }}
                  </p>
                  <p class="text-xs text-gray-500">{{ formatDateTime(order.order_date) }}</p>
                  <p class="text-xs text-gray-600">{{ formatPrice(order.final_amount) }}</p>
                </router-link>
              </div>
              <router-link 
                to="/admin/order" 
                class="block text-center text-sm text-customOrange font-medium mt-2 hover:underline"
                @click="closeNotifications"
              >
                Xem tất cả đơn hàng ({{ unprocessedOrdersCount }})
              </router-link>
            </div>
            <div v-else class="text-sm text-gray-500 mt-2">
              Không có đơn hàng mới.
            </div>
          </div>
        </div>
      </div>

      <!-- User Profile -->
      <div class="flex items-center space-x-2 cursor-pointer">
        <img src="@/assets/admin.png" alt="User" class="w-10 h-10 rounded-full border" />
        <div>
          <p class="text-gray-700 font-medium">Administrator</p>
          <p class="text-gray-500 text-sm">ID: 1234567</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { far } from '@fortawesome/free-regular-svg-icons';

library.add(far);

export default {
  name: 'Header',
  components: {
    FontAwesomeIcon,
  },
  data() {
    return {
      allOrders: [],
      showNotifications: false,
      pollingInterval: null,
      isLoading: false,
      MAX_DISPLAYED_ORDERS: 5
    };
  },
  computed: {
    unprocessedOrders() {
      return this.allOrders.filter(order => 
        order.order_id && 
        order.is_processed == 0
      );
    },
    unprocessedOrdersCount() {
      return this.unprocessedOrders.length;
    },
    hasUnprocessedOrders() {
      return this.unprocessedOrdersCount > 0 && !this.isLoading;
    },
    displayedOrders() {
      return this.unprocessedOrders.slice(0, this.MAX_DISPLAYED_ORDERS);
    }
  },
  mounted() {
    this.fetchOrders();
    this.setupPolling();
  },
  beforeDestroy() {
    this.clearPolling();
  },
  methods: {
    async fetchOrders() {
      this.isLoading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/orders/');
        this.allOrders = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error('Lỗi khi lấy danh sách đơn hàng:', error);
        this.allOrders = [];
      } finally {
        this.isLoading = false;
      }
    },
    setupPolling() {
      this.pollingInterval = setInterval(() => {
        if (!this.showNotifications) {
          this.fetchOrders();
        }
      }, 30000); // 30 giây
    },
    clearPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
      }
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
      if (this.showNotifications) {
        this.fetchOrders();
      }
    },
    closeNotifications() {
      this.showNotifications = false;
    },
    formatPrice(price) {
      if (price === null || price === undefined) return '0 ₫';
      const amount = typeof price === 'string' ? parseFloat(price) : price;
      return amount.toLocaleString('vi-VN', {
        style: 'currency',
        currency: 'VND'
      });
    },
    formatDateTime(dateString) {
      if (!dateString) return '';
      try {
        const date = new Date(dateString);
        return date.toLocaleString('vi-VN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });
      } catch (e) {
        console.error('Lỗi định dạng ngày giờ:', e);
        return dateString;
      }
    }
  }
};
</script>