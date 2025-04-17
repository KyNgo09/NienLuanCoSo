<template>
  <div class="flex flex-col min-h-screen w-full bg-gray-50">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="p-6">
        <!-- Danh sách đơn hàng -->
        <h2 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-2">Danh sách đơn hàng</h2>

        <!-- Bộ lọc -->
        <div class="mb-6 flex items-center gap-4">
          <input type="checkbox" v-model="showUnprocessedOnly" @change="filterOrders"
            class="w-5 h-5 text-customOrange focus:ring-customOrange focus:ring-2">
          <label for="unprocessed-filter" class="text-gray-700 font-medium">Hiển thị đơn hàng chưa xử lý</label>
        </div>

        <!-- Loading Indicator -->
        <div v-if="isLoading" class="text-center text-gray-500 italic animate-pulse">
          Đang tải đơn hàng...
        </div>

        <!-- Danh sách đơn hàng -->
        <div v-else-if="paginatedOrders.length" class="overflow-x-auto bg-white  rounded-lg">
          <table class="min-w-full border-collapse">
            <thead>
              <tr class="bg-customOrange text-white">
                <th class="py-3 px-6 border">Mã đơn hàng</th>
                <th class="py-3 px-6 border">Khách hàng</th>
                <th class="py-3 px-6 border">Loại khách</th>
                <th class="py-3 px-6 border">Ngày đặt</th>
                <th class="py-3 px-6 border">Tổng tiền</th>
                <th class="py-3 px-6 border">Phương thức thanh toán</th>
                <th class="py-3 px-6 border">Đã xử lý</th>
              </tr>
            </thead>
            <tbody class="text-gray-700">
              <tr v-for="order in paginatedOrders[currentPage]" :key="order.order_id"
                class="odd:bg-white even:bg-gray-100 hover:bg-orange-100 transition cursor-pointer"
                @click="selectOrder(order)">
                <td class="py-3 px-6 border text-center">{{ order.order_id }}</td>
                <td class="py-3 px-6 border text-center">{{ order.customer?.name || 'Khách vãng lai' }}</td>
                <td class="py-3 px-6 border text-center">{{ order.is_registered ? 'Thành viên' : 'Khách vãng lai' }}
                </td>
                <td class="py-3 px-6 border text-center">{{ formatDate(order.order_date) }}</td>
                <td class="py-3 px-6 border text-center">{{ formatPrice(order.final_amount) }}</td>
                <td class="py-3 px-6 border text-center">{{ order.payment_method }}</td>
                <td class="py-3 px-6 border text-center">
                  <input type="checkbox" v-model="order.is_processed"
                    @change="updateProcessed(order.order_id, order.is_processed)" @click.stop
                    class="w-5 h-5 text-customOrange focus:ring-customOrange focus:ring-2" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-else class="text-center text-gray-500 italic mt-6">
          Không có đơn hàng nào.
        </div>

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
                  <p><strong>Loại khách hàng:</strong> {{ selectedOrder.is_registered ? 'Thành viên' : 'Khách vãng lai'
                  }}</p>
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
                <p class="text-lg font-semibold"><strong>Tổng tiền:</strong> {{ formatPrice(selectedOrder.final_amount)
                }}</p>
              </div>
            </div>
            <!-- Checkbox xử lý và nút hành động -->
            <div class="mt-8 flex items-center gap-4">
              <input type="checkbox" v-model="selectedOrder.is_processed"
                @change="updateProcessed(selectedOrder.order_id, selectedOrder.is_processed)"
                class="w-5 h-5 text-customOrange focus:ring-customOrange focus:ring-2">
              <label class="text-gray-700 font-medium">Đã xử lý</label>
            </div>
            <div class="mt-8 flex justify-end gap-4">
              <button @click="exportPDF"
                class="bg-customOrange text-white px-6 py-3 rounded-lg font-bold hover:bg-orange-600 transition"
                :disabled="!canExportPDF">
                Xuất hóa đơn điện tử
              </button>
              <button @click="closeModal"
                class="bg-gray-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-gray-600 transition">
                Đóng
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import LeftSidebar from "@/components/admin/layout/left_sidebar.vue";
import Header from "@/components/admin/layout/header.vue";
import axios from 'axios';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable'; // Import autoTable

export default {
  components: {
    Header,
    LeftSidebar,
  },
  data() {
    return {
      orders: [],
      filteredOrders: [],
      isLoading: false,
      selectedOrder: null,
      orderDetails: [],
      canExportPDF: false,
      showModal: false,
      showUnprocessedOnly: false,
      currentPage: 0,
      itemsPerPage: 10,
      jsPDF: null,
    };
  },
  computed: {
    paginatedOrders() {
      const pages = [];
      const ordersToDisplay = this.showUnprocessedOnly ? this.filteredOrders : this.orders;
      for (let i = 0; i < ordersToDisplay.length; i += this.itemsPerPage) {
        pages.push(ordersToDisplay.slice(i, i + this.itemsPerPage));
      }
      return pages;
    },
    totalPages() {
      return this.paginatedOrders.length;
    },
  },
  async mounted() {
    try {
      this.jsPDF = jsPDF;
      this.canExportPDF = true; // Không cần gọi autoTable(this.jsPDF)
    } catch (error) {
      console.error('Lỗi khi khởi tạo jsPDF:', error);
      alert('Không thể tải thư viện xuất PDF. Vui lòng kiểm tra cài đặt.');
    }
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      this.isLoading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/orders/');
        console.log('Dữ liệu đơn hàng từ API:', response.data);
        this.orders = Array.isArray(response.data) ? response.data : [];
        this.filterOrders();
      } catch (error) {
        console.error('Lỗi khi lấy danh sách đơn hàng:', error);
        if (error.response) {
          console.error('Mã lỗi:', error.response.status);
          console.error('Chi tiết lỗi:', error.response.data);
          alert(`Lỗi khi tải đơn hàng: ${error.response.data.message || 'Không thể kết nối đến server'}`);
        } else {
          alert('Lỗi mạng hoặc server không phản hồi.');
        }
      } finally {
        this.isLoading = false;
      }
    },
    filterOrders() {
      if (this.showUnprocessedOnly) {
        this.filteredOrders = this.orders.filter(order => !order.is_processed);
      } else {
        this.filteredOrders = [...this.orders];
      }
      this.currentPage = 0;
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
    async updateProcessed(orderId, isProcessed) {
      try {
        await axios.patch(`http://127.0.0.1:8000/api/orders/${orderId}/`, { is_processed: isProcessed });
        this.orders = this.orders.map(o =>
          o.order_id === orderId ? { ...o, is_processed: isProcessed } : o
        );
        this.filterOrders();
      } catch (error) {
        console.error('Lỗi khi cập nhật trạng thái:', error);
        alert('Cập nhật trạng thái thất bại! Sản phẩm không còn đủ hàng');
        this.orders = this.orders.map(o =>
          o.order_id === orderId ? { ...o, is_processed: !isProcessed } : o
        );
        if (this.selectedOrder?.order_id === orderId) {
          this.selectedOrder.is_processed = !isProcessed;
        }
        this.filterOrders();
      }
    },
    exportPDF() {
      if (!this.canExportPDF || !this.jsPDF) {
        alert('Thư viện PDF không khả dụng. Vui lòng kiểm tra cài đặt.');
        return;
      }
      const doc = new this.jsPDF();
      // Đảm bảo font mặc định được thiết lập
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(12);

      // Thêm thông tin hóa đơn
      doc.text(`Hóa đơn #${this.selectedOrder.order_id}`, 20, 20);
      doc.text(`Khách hàng: ${this.selectedOrder.customer?.name || 'Khách vãng lai'}`, 20, 30);
      doc.text(`Ngày đặt: ${this.formatDate(this.selectedOrder.order_date)}`, 20, 40);
      doc.text(`Phương thức thanh toán: ${this.selectedOrder.payment_method}`, 20, 50);
      doc.text(`Địa chỉ: ${this.selectedOrder.customer?.address || 'N/A'}`, 20, 60);

      // Tạo bảng với autoTable
      const tableData = this.orderDetails.map(item => [
        item.product?.name || 'Sản phẩm không xác định',
        item.quantity,
        this.formatPrice(item.unit_price),
        this.formatPrice(item.sub_total),
      ]);
      autoTable(doc, {
        head: [['Sản phẩm', 'Số lượng', 'Đơn giá', 'Thành tiền']],
        body: tableData,
        startY: 70,
        theme: 'grid',
        styles: { font: 'helvetica', fontSize: 10 },
      });

      // Thêm thông tin tổng tiền
      const finalY = doc.lastAutoTable.finalY || 70;
      doc.text(`Tổng tiền: ${this.formatPrice(this.selectedOrder.total_amount)}`, 20, finalY + 10);
      doc.text(`Giảm giá: ${this.formatPrice(this.selectedOrder.discount)}`, 20, finalY + 20);
      doc.text(`Thành tiền: ${this.formatPrice(this.selectedOrder.final_amount)}`, 20, finalY + 30);

      // Lưu file PDF
      doc.save(`hoa_don_${this.selectedOrder.order_id}.pdf`);
    },
  },
};
</script>