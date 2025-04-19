<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="p-6">
        <!-- Danh sách đơn hàng -->
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách đơn hàng</h2>

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
                class="odd:bg-white even:bg-gray-100 hover:bg-gray-200 transition cursor-pointer"
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
import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";

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
      this.canExportPDF = true;
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
    async exportPDF() {
  if (!this.canExportPDF || !this.jsPDF) {
    alert('Thư viện PDF không khả dụng. Vui lòng kiểm tra cài đặt.');
    return;
  }

  try {
    // 1. Tạo document
    const doc = new this.jsPDF({
      orientation: 'portrait',
      unit: 'mm'
    });

    // 2. Sử dụng OpenSans đã được import
    const fontName = 'opensans';
    
    // Kiểm tra và thêm font nếu chưa có
    if (!this.openSansAdded) {
      // Lấy font từ DOM (cần đảm bảo font đã load trong index.html)
      const openSansFont = this.getFontFromDOM('opensans');
      if (openSansFont) {
        doc.addFileToVFS('OpenSans.ttf', openSansFont);
        doc.addFont('OpenSans.ttf', fontName, 'normal');
        this.openSansAdded = true;
      }
    }

    // 3. Thiết lập font chính
    doc.setFont(fontName);
    doc.setFontSize(12);

    // 4. Tiêu đề hóa đơn
    doc.setFontSize(20);
    doc.setTextColor(0, 0, 0);
    doc.text('HÓA ĐƠN ĐIỆN TỬ', 105, 20, { align: 'center' });
    
    // 5. Thông tin đơn hàng
    doc.setFontSize(14);
    doc.setTextColor(0, 0, 0);
    doc.text(`Mã đơn hàng: #${this.selectedOrder.order_id}`, 105, 30, { align: 'center' });

    // 6. Thông tin khách hàng
    doc.setFontSize(12);
    const yStart = 40;
    doc.text(`Khách hàng: ${this.selectedOrder.customer?.name || 'Khách vãng lai'}`, 20, yStart);
    doc.text(`Loại khách: ${this.selectedOrder.is_registered ? 'Thành viên' : 'Khách vãng lai'}`, 20, yStart + 6);
    doc.text(`Số điện thoại: ${this.selectedOrder.customer?.phone || 'N/A'}`, 20, yStart + 12);
    doc.text(`Email: ${this.selectedOrder.customer?.email || 'N/A'}`, 20, yStart + 18);
    
    // 7. Thông tin đơn hàng
    doc.text(`Ngày đặt: ${this.formatDate(this.selectedOrder.order_date)}`, 120, yStart);
    doc.text(`Phương thức thanh toán: ${this.selectedOrder.payment_method}`, 120, yStart + 6);
    doc.text(`Địa chỉ: ${this.selectedOrder.customer?.address || 'N/A'}`, 120, yStart + 12);

    // 8. Bảng chi tiết sản phẩm
    const tableData = this.orderDetails.map((item, index) => [
      index + 1,
      item.product?.name || 'Sản phẩm không xác định',
      item.quantity,
      this.formatPrice(item.unit_price),
      this.formatPrice(item.sub_total)
    ]);

    doc.autoTable({
      head: [['STT', 'Sản phẩm', 'SL', 'Đơn giá', 'Thành tiền']],
      body: tableData,
      startY: yStart + 30,
      margin: { left: 20, right: 20 },
      headStyles: {
        fillColor: [238, 238, 238],
        textColor: [0, 0, 0],
        fontStyle: 'bold',
        font: fontName
      },
      styles: {
        font: fontName,
        fontSize: 10,
        cellPadding: 3
      },
      columnStyles: {
        0: { cellWidth: 15 },
        1: { cellWidth: 'auto' },
        2: { cellWidth: 15 },
        3: { cellWidth: 30 },
        4: { cellWidth: 30 }
      }
    });

    // 9. Tổng kết
    const finalY = doc.lastAutoTable.finalY + 10;
    
    doc.setFontSize(12);
    doc.text(`Thành tiền: ${this.formatPrice(this.selectedOrder.total_amount)}`, 140, finalY, { align: 'right' });
    doc.text(`Giảm giá: ${this.formatPrice(this.selectedOrder.discount)}`, 140, finalY + 6, { align: 'right' });
    
    doc.setFontSize(14);
    doc.setFont(fontName, 'bold');
    doc.text(`Tổng cộng: ${this.formatPrice(this.selectedOrder.final_amount)}`, 140, finalY + 14, { align: 'right' });

    // 10. Footer
    doc.setFontSize(10);
    doc.setTextColor(100, 100, 100);
    doc.text('Cảm ơn quý khách đã sử dụng dịch vụ!', 105, 280, { align: 'center' });
    doc.text(`Ngày xuất: ${new Date().toLocaleDateString('vi-VN')}`, 105, 285, { align: 'center' });

    // Lưu file PDF
    doc.save(`hoa_don_${this.selectedOrder.order_id}.pdf`);
  } catch (error) {
    console.error('Lỗi khi xuất PDF:', error);
    alert('Đã xảy ra lỗi khi xuất PDF. Vui lòng thử lại.');
  }
},

// Hàm lấy font từ DOM
getFontFromDOM(fontFamily) {
  try {
    // Tìm kiếm font-face OpenSans đã được định nghĩa trong CSS
    const styleSheets = document.styleSheets;
    for (let i = 0; i < styleSheets.length; i++) {
      const rules = styleSheets[i].cssRules;
      for (let j = 0; j < rules.length; j++) {
        if (rules[j].type === CSSRule.FONT_FACE_RULE && 
            rules[j].style.fontFamily.includes(fontFamily)) {
          const src = rules[j].style.src;
          const urlMatch = src.match(/url\(["']?(.*?)["']?\)/);
          if (urlMatch && urlMatch[1]) {
            return this.loadFontAsBase64(urlMatch[1]);
          }
        }
      }
    }
    return null;
  } catch (error) {
    console.error('Lỗi khi lấy font từ DOM:', error);
    return null;
  }
},

// Hàm tải font và chuyển thành base64
async loadFontAsBase64(url) {
  try {
    const response = await fetch(url);
    const buffer = await response.arrayBuffer();
    return this.arrayBufferToBase64(buffer);
  } catch (error) {
    console.error('Lỗi khi tải font:', error);
    return null;
  }
},

// Hàm chuyển ArrayBuffer sang Base64
arrayBufferToBase64(buffer) {
  let binary = '';
  const bytes = new Uint8Array(buffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}
  },
};
</script>