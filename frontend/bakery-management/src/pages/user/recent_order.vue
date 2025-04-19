<template>
    <div class="flex flex-col min-h-screen w-full">
      <Header />
      <div class="flex flex-1 flex-col w-full">
        <div class="p-6 flex-1">
          <!-- Danh sách đơn hàng -->
          <h2 class="text-3xl font-bold mb-6 text-customBrown font-sansita">Đơn hàng gần đây</h2>
  
          <!-- Loading Indicator -->
          <div v-if="isLoading" class="text-center text-gray-500 italic animate-pulse">
            Đang tải đơn hàng...
          </div>
  
          <!-- Danh sách đơn hàng -->
          <div v-else-if="paginatedOrders.length" class="overflow-x-auto bg-white rounded-lg">
            <table class="min-w-full border-collapse">
              <thead>
                <tr class="bg-customOrange text-white">
                  <th class="py-3 px-6 border">Mã đơn hàng</th>
                  <th class="py-3 px-6 border">Ngày đặt</th>
                  <th class="py-3 px-6 border">Tổng tiền</th>
                  <th class="py-3 px-6 border">Phương thức thanh toán</th>
                  <th class="py-3 px-6 border">Đã xử lý</th>
                </tr>
              </thead>
              <tbody class="text-gray-700">
                <tr v-for="order in paginatedOrders[currentPage]" :key="order.order_id"
                  class="odd:bg-white even:bg-gray-100 hover:bg-gray-200 transition cursor-pointer"
                  @click="selectOrder(order)">
                  <td class="py-3 px-6 border text-center">{{ order.order_id }}</td>
                  <td class="py-3 px-6 border text-center">{{ formatDate(order.order_date) }}</td>
                  <td class="py-3 px-6 border text-center">{{ formatPrice(order.final_amount) }}</td>
                  <td class="py-3 px-6 border text-center">{{ order.payment_method }}</td>
                  <td class="py-3 px-6 border text-center">
                    <span>{{ order.is_processed ? 'Đã xử lý' : 'Chưa xử lý' }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
  
          <!-- Thông báo không có đơn hàng -->
          <div v-else class="text-center text-gray-500 italic mt-6">
            Không có đơn hàng nào.
          </div>
  
          <!-- Pagination -->
          <div class="mt-8 flex justify-center space-x-4">
            <button @click="currentPage = Math.max(currentPage - 1, 0)" :disabled="currentPage === 0"
              class="px-4 py-2 bg-gray-300 text-gray-600 rounded-lg hover:bg-gray-400 disabled:opacity-50">Trước</button>
            <button v-for="page in totalPages" :key="page" @click="currentPage = page - 1"
              :class="['px-4 py-2 rounded-lg', currentPage === page - 1 ? 'bg-customOrange text-white' : 'bg-gray-300 hover:bg-gray-400']">
              {{ page }}
            </button>
            <button @click="currentPage = Math.min(currentPage + 1, totalPages - 1)"
              :disabled="currentPage === totalPages - 1"
              class="px-4 py-2 bg-gray-300 text-gray-600 rounded-lg hover:bg-gray-400 disabled:opacity-50">Sau</button>
          </div>
  
          <!-- Modal chi tiết đơn hàng -->
          <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white p-8 rounded-lg shadow-2xl max-w-3xl w-full max-h-[80vh] overflow-y-auto">
              <h2 class="text-2xl font-bold mb-6 text-gray-800">Chi tiết đơn hàng #{{ selectedOrder.order_id }}</h2>
              <div id="invoice" class="border p-6 bg-gray-50 rounded-lg">
                <h3 class="text-3xl font-semibold mb-6 text-center">Hóa đơn</h3>
                <!-- Chi tiết hóa đơn -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <p><strong>Mã đơn hàng:</strong> {{ selectedOrder.order_id }}</p>
                    <p><strong>Khách hàng:</strong> {{ selectedOrder.customer?.name || 'Khách vãng lai' }}</p>
                    <p><strong>Loại khách hàng:</strong> {{ selectedOrder.is_registered ? 'Thành viên' : 'Khách vãng lai' }}</p>
                    <p><strong>Số điện thoại:</strong> {{ selectedOrder.customer?.phone || 'N/A' }}</p>
                    <p><strong>Email:</strong> {{ selectedOrder.customer?.email || 'N/A' }}</p>
                  </div>
                  <div>
                    <p><strong>Địa chỉ:</strong> {{ selectedOrder.customer?.address || 'N/A' }}</p>
                    <p><strong>Ngày đặt:</strong> {{ formatDate(selectedOrder.order_date) }}</p>
                    <p><strong>Phương thức thanh toán:</strong> {{ selectedOrder.payment_method }}</p>
                  </div>
                </div>
                <h4 class="text-lg font-semibold mb-4 text-gray-700">Sản phẩm</h4>
                <table class="min-w-full border">
                  <thead class="bg-gray-200">
                    <tr>
                      <th class="py-2 px-4 border">STT</th>
                      <th class="py-2 px-4 border">Sản phẩm</th>
                      <th class="py-2 px-4 border">SL</th>
                      <th class="py-2 px-4 border">Đơn giá</th>
                      <th class="py-2 px-4 border">Thành tiền</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in orderDetails" :key="item.order_detail_id" class="hover:bg-gray-100">
                      <td class="py-2 px-4 border text-center">{{ index + 1 }}</td>
                      <td class="py-2 px-4 border text-center">{{ item.product?.name || 'Sản phẩm không xác định' }}</td>
                      <td class="py-2 px-4 border text-center">{{ item.quantity }}</td>
                      <td class="py-2 px-4 border text-center">{{ formatPrice(item.unit_price) }}</td>
                      <td class="py-2 px-4 border text-center">{{ formatPrice(item.sub_total) }}</td>
                    </tr>
                  </tbody>
                </table>
                <!-- Tổng tiền, Giảm giá, Thành tiền -->
                <div class="mt-6 text-right">
                  <p><strong>Thành tiền:</strong> {{ formatPrice(selectedOrder.total_amount) }}</p>
                  <p><strong>Giảm giá:</strong> {{ formatPrice(selectedOrder.discount) }}</p>
                  <p class="text-lg font-semibold"><strong>Tổng tiền:</strong> {{ formatPrice(selectedOrder.final_amount) }}</p>
                </div>
              </div>
              <!-- Nút hành động -->
              <div class="mt-8 flex justify-end gap-4">
                <button @click="closeModal"
                  class="bg-gray-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-gray-600 transition">
                  Đóng
                </button>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </div>
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
    data() {
      return {
        orders: [],
        isLoading: false,
        selectedOrder: null,
        orderDetails: [],
        showModal: false,
        currentPage: 0,
        itemsPerPage: 10,
      };
    },
    computed: {
      paginatedOrders() {
        const pages = [];
        for (let i = 0; i < this.orders.length; i += this.itemsPerPage) {
          pages.push(this.orders.slice(i, i + this.itemsPerPage));
        }
        return pages;
      },
      totalPages() {
        return this.paginatedOrders.length;
      },
    },
    async mounted() {
      await this.fetchOrders();
    },
    methods: {
        async fetchOrders() {
  this.isLoading = true;
  const userId = localStorage.getItem('user_id');
  console.log('Người dùng ID:', userId);
  
  if (!userId) {
    alert('Vui lòng đăng nhập để xem đơn hàng.');
    this.isLoading = false;
    return;
  }
  
  try {
    // Lấy danh sách khách hàng
    console.log('Đang lấy thông tin khách hàng...');
    const customerResponse = await axios.get(`http://127.0.0.1:8000/api/customers/?user_id=${userId}`);
    console.log('Danh sách khách hàng:', customerResponse.data);
    
    // Tìm khách hàng có user khớp với userId
    const customer = customerResponse.data.find(cust => cust.user === parseInt(userId));
    console.log('Khách hàng tìm được:', customer);
    
    if (!customer) {
      throw new Error('Không tìm thấy khách hàng tương ứng với user_id này.');
    }
    
    const customerId = customer.customer_id;
    console.log('Customer ID cần lọc:', customerId);
    
    // Lấy TẤT CẢ đơn hàng (tạm thời)
    console.log('Đang lấy tất cả đơn hàng...');
    const response = await axios.get(`http://127.0.0.1:8000/api/orders/`);
    console.log('Tất cả đơn hàng từ API:', response.data);
    
    // Filter phía client theo customer_id
    const filteredOrders = Array.isArray(response.data) 
      ? response.data.filter(order => {
          const match = order.customer?.customer_id === customerId;
          console.log(`Order ${order.order_id} - Customer: ${order.customer?.customer_id} - Match: ${match}`);
          return match;
        })
      : [];
    
    console.log('Đơn hàng đã lọc:', filteredOrders);
    this.orders = filteredOrders;
    
    if (filteredOrders.length === 0) {
      console.warn('Không tìm thấy đơn hàng nào cho customer_id này');
    }
  } catch (error) {
    console.error('Lỗi khi lấy danh sách đơn hàng:', error);
    if (error.response) {
      console.error('Chi tiết lỗi:', {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      });
      alert(`Lỗi khi tải đơn hàng: ${error.response.data.detail || 'Lỗi server'}`);
    } else {
      alert(error.message || 'Lỗi kết nối mạng');
    }
  } finally {
    this.isLoading = false;
  }
},
      async selectOrder(order) {
        this.selectedOrder = order;
        this.showModal = true;
        await this.fetchOrderDetails(order.order_id);
      },
      async fetchOrderDetails(orderId) {
        try {
          const response = await axios.get(`http://127.0.0.1:8000/api/order_details/?order=${orderId}`);
          console.log('Dữ liệu chi tiết đơn hàng:', response.data);
          this.orderDetails = response.data;
        } catch (error) {
          console.error('Lỗi khi lấy chi tiết sản phẩm:', error);
          this.orderDetails = [];
        }
      },
      closeModal() {
        this.showModal = false;
        this.selectedOrder = null;
        this.orderDetails = [];
      },
      formatPrice(price) {
        return parseFloat(price).toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
      },
      formatDate(date) {
        return new Date(date).toLocaleDateString('vi-VN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
        });
      },
    },
  };
  </script>