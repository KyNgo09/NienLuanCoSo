<template>
    <div class="flex flex-col min-h-screen w-full">
        <Header />
        <div class="flex flex-1 w-full">
            <LeftSidebar />
            <div class="p-4 flex-1">
                <h2 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-4">Nhà cung cấp</h2>

                <!-- Form thêm nhà cung cấp -->
                <form @submit.prevent="createSupplier" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <input v-model="newSupplier.name" placeholder="Tên nhà cung cấp"
                        class="border p-2 text-black rounded" />
                    <input v-model="newSupplier.phone" placeholder="Số điện thoại"
                        class="border p-2 text-black rounded" />
                    <input v-model="newSupplier.email" placeholder="Email" class="border p-2 text-black rounded" />
                    <input v-model="newSupplier.address" placeholder="Địa chỉ" class="border p-2 text-black rounded" />
                    <div class="md:col-span-2">
                        <button type="submit" class="bg-customOrange text-white px-4 py-2 rounded font-bold">
                            Thêm nhà cung cấp
                        </button>
                    </div>
                </form>

                <!-- Danh sách nhà cung cấp -->
                <table class="w-full border-collapse border border-gray-300 rounded overflow-hidden">
                    <thead>
                        <tr class="bg-customOrange text-white text-left">
                            <th class="px-4 py-2 border">STT</th>
                            <th class="px-4 py-2 border">Tên</th>
                            <th class="px-4 py-2 border">SĐT</th>
                            <th class="px-4 py-2 border">Email</th>
                            <th class="px-4 py-2 border">Địa chỉ</th>
                            <th class="px-4 py-2 border">Thao tác</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(supplier, index) in suppliers" :key="supplier.supplier_id"
                            class="even:bg-gray-100 hover:bg-gray-200 transition text-gray-900">
                            <td class="px-4 py-2 border">{{ index + 1 }}</td>
                            <td class="px-4 py-2 border">{{ supplier.name }}</td>
                            <td class="px-4 py-2 border">{{ supplier.phone }}</td>
                            <td class="px-4 py-2 border">{{ supplier.email }}</td>
                            <td class="px-4 py-2 border">{{ supplier.address }}</td>
                            <td class="px-4 py-2 border">
                                <button @click="deleteSupplier(supplier.supplier_id)"
                                    class="text-red-500 hover:text-red-700 font-semibold">
                                    Xóa
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="mt-10">
                    <h2 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-4">Nguyên liệu</h2>

                    <form @submit.prevent="createIngredient" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <input v-model="newIngredient.name" placeholder="Tên nguyên liệu"
                            class="w-full border p-2 rounded text-black" />

                        <select v-model="newIngredient.unit" class="w-full border p-2 rounded text-black">
                            <option value="">-- Chọn đơn vị --</option>
                            <option v-for="unit in units" :key="unit.unit_id" :value="unit.unit_id">
                                {{ unit.name }}
                            </option>
                        </select>

                        <input v-model.number="newIngredient.stock_quantity" type="number" step="0.01"
                            placeholder="Số lượng" class="w-full border p-2 rounded text-black" />

                        <select v-model="newIngredient.supplier" class="w-full border p-2 rounded text-black">
                            <option value="">-- Chọn nhà cung cấp --</option>
                            <option v-for="supplier in suppliers" :key="supplier.supplier_id"
                                :value="supplier.supplier_id">
                                {{ supplier.name }}
                            </option>
                        </select>
                        <div class="md:col-span-2">
                            <button type="submit" class="bg-customOrange text-white px-4 py-2 rounded font-bold">
                                Thêm nguyên liệu
                            </button>
                        </div>
                    </form>
                    <!-- Danh sách nguyên liệu -->
                    <table class="w-full border-collapse border border-gray-300 rounded overflow-hidden">
                        <thead>
                            <tr class="bg-customOrange text-white text-left">
                                <th class="px-4 py-2 border">STT</th>
                                <th class="px-4 py-2 border">Tên</th>
                                <th class="px-4 py-2 border">Số lượng</th>
                                <th class="px-4 py-2 border">Đơn vị</th>
                                <th class="px-4 py-2 border">Nhà cung cấp</th>
                                <th class="px-4 py-2 border">Thao tác</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(ingredient, index) in ingredients" :key="ingredient.ingredient_id"
                                class="even:bg-gray-100 hover:bg-gray-200 transition text-gray-900">
                                <td class="px-4 py-2 border">{{ index + 1 }}</td>
                                <td class="px-4 py-2 border">{{ ingredient.name }}</td>
                                <td class="px-4 py-2 border">{{ ingredient.stock_quantity }}</td>
                                <td class="px-4 py-2 border">{{ getUnitName(ingredient.unit) }}</td>
                                <td class="px-4 py-2 border">{{ getSupplierName(ingredient.supplier) }}</td>
                                <td class="px-4 py-2 border">
                                    <button @click="deleteIngredient(ingredient.ingredient_id)"
                                        class="text-red-500 hover:text-red-700 font-semibold">
                                        Xóa
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Header from "@/components/admin/layout/header.vue";
import LeftSidebar from "@/components/admin/layout/left_sidebar.vue";
import axios from "axios";

export default {
    components: { Header, LeftSidebar },
    data() {
        return {
            // Nhà cung cấp
            suppliers: [],
            newSupplier: {
                name: "",
                phone: "",
                email: "",
                address: ""
            },

            // Nguyên liệu
            ingredients: [],
            newIngredient: {
                name: "",
                stock_quantity: "",
                unit: "",
                supplier: ""
            },

            // Đơn vị đo lường
            units: []
        };
    },
    methods: {
        // ==== NHÀ CUNG CẤP ====
        async fetchSuppliers() {
            try {
                const res = await axios.get("http://127.0.0.1:8000/api/suppliers/");
                this.suppliers = res.data;
            } catch (error) {
                console.error("Lỗi khi lấy danh sách nhà cung cấp:", error);
            }
        },
        async createSupplier() {
            if (!this.newSupplier.name || !this.newSupplier.phone || !this.newSupplier.email || !this.newSupplier.address) {
                alert("Vui lòng điền đầy đủ thông tin nhà cung cấp!");
                return;
            }
            try {
                await axios.post("http://127.0.0.1:8000/api/suppliers/", this.newSupplier);
                this.newSupplier = { name: "", phone: "", email: "", address: "" };
                await this.fetchSuppliers();
                alert("Thêm nhà cung cấp thành công!");
            } catch (error) {
                console.error("Lỗi khi thêm nhà cung cấp:", error);
            }
        },
        async deleteSupplier(id) {
            if (!confirm("Bạn có chắc muốn xóa nhà cung cấp này?")) return;
            try {
                await axios.delete(`http://127.0.0.1:8000/api/suppliers/${id}/`);
                this.suppliers = this.suppliers.filter(s => s.supplier_id !== id);
                alert("Xóa thành công!");
            } catch (error) {
                console.error("Lỗi khi xóa nhà cung cấp:", error);
            }
        },

        // ==== ĐƠN VỊ ====
        async fetchUnits() {
            try {
                const res = await axios.get("http://127.0.0.1:8000/api/units/");
                this.units = res.data;
            } catch (error) {
                console.error("Lỗi khi lấy đơn vị:", error);
            }
        },

        // ==== NGUYÊN LIỆU ====
        async fetchIngredients() {
            try {
                const res = await axios.get("http://127.0.0.1:8000/api/ingredients/");
                this.ingredients = res.data;
            } catch (error) {
                console.error("Lỗi khi lấy danh sách nguyên liệu:", error);
            }
        },
        async createIngredient() {
            if (!this.newIngredient.name || !this.newIngredient.unit || !this.newIngredient.stock_quantity || !this.newIngredient.supplier) {
                alert("Vui lòng điền đầy đủ thông tin nguyên liệu!");
                return;
            }
            try {
                await axios.post("http://127.0.0.1:8000/api/ingredients/", this.newIngredient);
                this.newIngredient = { name: "", stock_quantity: "", unit: "", supplier: "" };
                await this.fetchIngredients();
                alert("Thêm nguyên liệu thành công!");
            } catch (error) {
                console.error("Lỗi khi thêm nguyên liệu:", error);
            }
        },
        async deleteIngredient(id) {
            if (!confirm("Bạn có chắc muốn xóa nguyên liệu này?")) return;
            try {
                await axios.delete(`http://127.0.0.1:8000/api/ingredients/${id}/`);
                alert("Xóa thành công!");
                this.ingredients = this.ingredients.filter(ing => ing.ingredient_id !== id);
            } catch (error) {
                console.error("Lỗi khi xóa nhà nguyên liệu:", error);
            }
        },
        getUnitName(unitId) {
            const unit = this.units.find(u => u.unit_id === unitId);
            return unit ? unit.name : "Không xác định";
        },
        getSupplierName(supplierId) {
            const supplier = this.suppliers.find(s => s.supplier_id === supplierId);
            return supplier ? supplier.name : "Không xác định";
        }
    },
    mounted() {
        this.fetchSuppliers();
        this.fetchUnits();
        this.fetchIngredients();
    }
};
</script>
