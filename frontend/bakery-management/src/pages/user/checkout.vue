<template>
    <div class="min-h-screen flex flex-col">
        <Header />
        <div class="container mx-auto p-4">
            <h1 class="text-4xl font-bold mb-6 text-customBrown font-sansita">Đặt hàng</h1>
            <div v-if="cart.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Form đặt hàng -->
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-2xl font-semibold mb-4 text-gray-700">Thông tin đặt hàng</h2>
                    <form @submit.prevent="submitOrder">
                        <div class="mb-4">
                            <label class="block text-gray-700 mb-1">Họ tên *</label>
                            <input v-model="form.name" type="text" class="w-full border rounded-lg px-3 py-2"
                                required />
                        </div>
                        <div class="mb-4">
                            <label class="block text-gray-700 mb-1">Số điện thoại *</label>
                            <input v-model="form.phone" type="tel" pattern="[0-9]{10}"
                                class="w-full border rounded-lg px-3 py-2" required />
                        </div>
                        <div class="mb-4">
                            <label class="block text-gray-700 mb-1">Email</label>
                            <input v-model="form.email" type="email" class="w-full border rounded-lg px-3 py-2" />
                        </div>
                        <div class="mb-4">
                            <label class="block text-gray-700 mb-1">Địa chỉ *</label>
                            <select v-model="form.district" class="w-full border rounded-lg px-3 py-2 mb-2" required
                                @change="updateWards">
                                <option value="" disabled>Chọn quận/huyện</option>
                                <option v-for="district in districts" :key="district.id" :value="district.id">
                                    {{ district.name }}
                                </option>
                            </select>
                            <select v-model="form.ward" class="w-full border rounded-lg px-3 py-2" required
                                :disabled="!form.district">
                                <option value="" disabled>Chọn phường/xã</option>
                                <option v-for="ward in wards" :key="ward.id" :value="ward.id">
                                    {{ ward.name }}
                                </option>
                            </select>
                            <input v-model="form.addressDetail" type="text"
                                class="w-full border rounded-lg px-3 py-2 mt-2" placeholder="Số nhà, tên đường"
                                required />
                        </div>
                        <div class="mb-4">
                            <label class="block text-gray-700 mb-1">Phương thức thanh toán *</label>
                            <div class="space-y-2">
                                <label class="flex items-center">
                                    <input type="radio" v-model="form.paymentMethod" value="Thanh toán khi nhận hàng"
                                        class="text-customOrange focus:ring-customOrange" required />
                                    <span class="ml-2 text-gray-700">Thanh toán khi nhận hàng</span>
                                </label>
                                <label class="flex items-center">
                                    <input type="radio" v-model="form.paymentMethod" value="Nhận tại cửa hàng"
                                        class="text-customOrange focus:ring-customOrange" />
                                    <span class="ml-2 text-gray-700">Nhận tại cửa hàng</span>
                                </label>
                            </div>
                        </div>
                        <button type="submit"
                            class="w-full bg-customOrange text-white font-semibold px-4 py-2 rounded hover:bg-orange-600">
                            Xác nhận đặt hàng
                        </button>
                    </form>
                </div>
                <!-- Giỏ hàng -->
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-2xl font-semibold mb-4 text-gray-700">Giỏ hàng của bạn</h2>
                    <div class="space-y-4">
                        <div v-for="item in cart" :key="item.product_id"
                            class="flex items-center justify-between border-b pb-4">
                            <div class="flex items-center space-x-4">
                                <img :src="item.image || 'https://placehold.co/150x150?text=No+Image'"
                                    alt="Hình ảnh sản phẩm" class="w-16 h-16 object-cover rounded" />
                                <div>
                                    <p class="text-lg font-semibold text-gray-700">{{ item.name }}</p>
                                    <p class="text-gray-600">{{ formatPrice(item.price) }} VND x {{ item.quantity }}</p>
                                </div>
                            </div>
                            <p class="text-gray-700 font-semibold">{{ formatPrice(item.price * item.quantity) }} VND</p>
                        </div>
                    </div>
                    <div class="mt-6">
                        <p class="text-xl font-semibold text-gray-700">
                            Tổng cộng: {{ formatPrice(totalPrice) }} VND
                        </p>
                    </div>
                </div>
            </div>
            <div v-else class="text-center text-gray-500">
                Giỏ hàng của bạn đang trống.
            </div>
        </div>
        <Footer />
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
            cart: JSON.parse(localStorage.getItem('cart')) || [],
            form: {
                name: '',
                phone: '',
                email: '',
                district: '',
                ward: '',
                addressDetail: '',
                paymentMethod: 'Thanh toán khi nhận hàng',
            },
            districts: [
                { id: 'ninh_kieu', name: 'Quận Ninh Kiều' },
                { id: 'cai_rang', name: 'Quận Cái Răng' },
                { id: 'binh_thuy', name: 'Quận Bình Thủy' },
                { id: 'o_mon', name: 'Quận Ô Môn' },
                { id: 'thot_not', name: 'Quận Thốt Nốt' },
                { id: 'co_do', name: 'Huyện Cờ Đỏ' },
                { id: 'phong_dien', name: 'Huyện Phong Điền' },
                { id: 'thoi_lai', name: 'Huyện Thới Lai' },
                { id: 'vinh_thanh', name: 'Huyện Vĩnh Thạnh' },
            ],
            wards: [],
            wardList: {
                ninh_kieu: [
                    { id: 'cai_khe', name: 'Phường Cái Khế' },
                    { id: 'an_binh', name: 'Phường An Bình' },
                    { id: 'an_hoa', name: 'Phường An Hòa' },
                    { id: 'an_khanh', name: 'Phường An Khánh' },
                    { id: 'xuan_khanh', name: 'Phường Xuân Khánh' },
                ],
                cai_rang: [
                    { id: 'le_binh', name: 'Phường Lê Bình' },
                    { id: 'hung_phu', name: 'Phường Hưng Phú' },
                ],
                binh_thuy: [
                    { id: 'binh_thuy', name: 'Phường Bình Thủy' },
                    { id: 'tra_an', name: 'Phường Trà An' },
                ],
                o_mon: [
                    { id: 'o_mon', name: 'Phường Ô Môn' },
                    { id: 'phuoc_thoi', name: 'Phường Phước Thới' },
                ],
                thot_not: [
                    { id: 'thot_not', name: 'Phường Thốt Nốt' },
                    { id: 'thuan_an', name: 'Phường Thuận An' },
                ],
                co_do: [
                    { id: 'co_do', name: 'Thị trấn Cờ Đỏ' },
                    { id: 'thoi_hung', name: 'Xã Thới Hưng' },
                ],
                phong_dien: [
                    { id: 'phong_dien', name: 'Thị trấn Phong Điền' },
                    { id: 'nhon_ai', name: 'Xã Nhơn Ái' },
                ],
                thoi_lai: [
                    { id: 'thoi_lai', name: 'Thị trấn Thới Lai' },
                    { id: 'tan_thanh', name: 'Xã Tân Thạnh' },
                ],
                vinh_thanh: [
                    { id: 'vinh_thanh', name: 'Thị trấn Vĩnh Thạnh' },
                    { id: 'thanh_an', name: 'Xã Thạnh An' },
                ],
            },
        };
    },
    computed: {
        totalPrice() {
            return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
        },
    },
    methods: {
        formatPrice(price) {
            if (!price && price !== 0) return '0';
            return parseInt(price).toLocaleString('vi-VN');
        },
        updateWards() {
            this.form.ward = '';
            this.wards = this.wardList[this.form.district] || [];
        },
        async submitOrder() {
            try {
                // Kiểm tra dữ liệu trước khi gửi
                if (!this.form.name || !this.form.phone || !this.form.district || !this.form.ward || !this.form.addressDetail) {
                    alert('Vui lòng điền đầy đủ thông tin bắt buộc.');
                    return;
                }
                if (!this.cart.length) {
                    alert('Giỏ hàng trống. Vui lòng thêm sản phẩm.');
                    return;
                }

                const customerData = JSON.parse(localStorage.getItem('customer')) || {};
                const userId = localStorage.getItem('user_id');
                const orderData = {
                    isLoggedIn: !!userId,
                    user_id: userId || null,
                    total_amount: Number(this.totalPrice),
                    discount: 0,
                    final_amount: Number(this.totalPrice),
                    payment_method: this.form.paymentMethod,
                    customer_name: this.form.name,
                    customer_phone: this.form.phone,
                    customer_email: this.form.email || '',
                    address: `${this.form.addressDetail}, ${this.getWardName()}, ${this.getDistrictName()}`,
                    items: this.cart.map(item => ({
                        product_id: Number(item.product_id),
                        quantity: Number(item.quantity),
                        unit_price: Number(item.price),
                        sub_total: Number(item.price * item.quantity),
                    })),
                };

                // Log dữ liệu để debug
                console.log('Giỏ hàng:', this.cart);
                console.log('Dữ liệu gửi đi:', JSON.stringify(orderData, null, 2));

                const response = await axios.post('http://127.0.0.1:8000/api/orders/', orderData, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.data.customer_id) {
                    localStorage.setItem('customer', JSON.stringify({
                        customer_id: response.data.customer_id,
                        name: this.form.name,
                        phone: this.form.phone,
                        email: this.form.email || '',
                        address: orderData.address,
                        loyalty_point: response.data.loyalty_point || 0,
                    }));
                }

                alert(`Đặt hàng thành công! Mã đơn hàng: ${response.data.order_id}`);
                localStorage.removeItem('cart');
                this.cart = [];
                this.$router.push('/products');
            } catch (error) {
                console.error('Lỗi khi đặt hàng:', error);
                const errorMessage = error.response?.data?.message || JSON.stringify(error.response?.data) || 'Đặt hàng thất bại. Vui lòng kiểm tra lại thông tin.';
                alert(`Lỗi: ${errorMessage}`);
                console.error('Chi tiết lỗi từ server:', error.response?.data);
            }
        },
        getDistrictName() {
            const district = this.districts.find(d => d.id === this.form.district);
            return district ? district.name : '';
        },
        getWardName() {
            const ward = this.wards.find(w => w.id === this.form.ward);
            return ward ? ward.name : '';
        },
    },
};
</script>

