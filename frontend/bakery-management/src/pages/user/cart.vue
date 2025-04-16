<template>
    <div class="min-h-screen flex flex-col">
        <Header />
        <div class="container mx-auto p-4">
            <h1 class="text-4xl font-bold mb-6 text-customBrown font-sansita">Giỏ hàng</h1>
            <router-link to="/products" class="text-blue-500 text-lg hover:underline mb-6 inline-block">
                ← Quay lại danh sách sản phẩm
            </router-link>
            <div v-if="cart.length > 0" class="bg-white rounded-lg shadow-lg p-6">
                <div class="space-y-4">
                    <div v-for="item in cart" :key="item.product_id"
                        class="flex items-center justify-between border-b pb-4">
                        <div class="flex items-center space-x-4">
                            <img :src="item.image || 'https://placehold.co/150x150?text=No+Image'"
                                alt="Hình ảnh sản phẩm" class="w-20 h-20 object-cover rounded" />
                            <div>
                                <router-link :to="{ name: 'ProductDetail', params: { id: item.product_id } }"
                                    class="text-lg font-semibold text-gray-700 hover:text-customOrange">
                                    {{ item.name }}
                                </router-link>
                                <p class="text-gray-600">{{ formatPrice(item.price) }} VND x {{ item.quantity }}</p>
                            </div>
                        </div>
                        <div class="flex items-center space-x-4">
                            <div class="flex items-center">
                                <button @click="updateQuantity(item.product_id, item.quantity - 1)"
                                    class="bg-customOrange text-white px-2 py-1 rounded-l hover:bg-orange-600"
                                    :disabled="item.quantity <= 1">-</button>
                                <input type="number" v-model.number="item.quantity" min="1"
                                    class="w-12 text-center border-t border-b border-gray-200" readonly />
                                <button @click="updateQuantity(item.product_id, item.quantity + 1)"
                                    class="bg-customOrange text-white px-2 py-1 rounded-r hover:bg-orange-600">+</button>
                            </div>
                            <button @click="removeFromCart(item.product_id)" class="text-red-500 hover:text-red-700">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="mt-6 flex justify-between items-center">
                    <p class="text-xl font-semibold text-gray-700">
                        Tổng cộng: {{ formatPrice(totalPrice) }} VND
                    </p>
                    <router-link to="/checkout"
                        class="bg-customOrange text-white font-semibold px-6 py-2 rounded hover:bg-orange-600">
                        Thanh toán
                    </router-link>
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

export default {
    components: {
        Header,
        Footer,
    },
    data() {
        return {
            cart: JSON.parse(localStorage.getItem('cart')) || [],
        };
    },
    computed: {
        totalPrice() {
            return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
        },
    },
    watch: {
        cart: {
            handler(newCart) {
                localStorage.setItem('cart', JSON.stringify(newCart));
                this.$root.$emit('cart-updated', newCart.length); // Phát sự kiện để Header cập nhật
            },
            deep: true,
        },
    },
    methods: {
        formatPrice(price) {
            if (!price && price !== 0) return '0';
            return parseInt(price).toLocaleString('vi-VN');
        },
        updateQuantity(productId, quantity) {
            if (quantity < 1) {
                this.removeFromCart(productId);
                return;
            }
            const item = this.cart.find(i => i.product_id === productId);
            if (item) {
                item.quantity = quantity;
                this.cart = [...this.cart]; // Trigger reactivity
            }
        },
        removeFromCart(productId) {
            this.cart = this.cart.filter(item => item.product_id !== productId);
        },
    },
};
</script>