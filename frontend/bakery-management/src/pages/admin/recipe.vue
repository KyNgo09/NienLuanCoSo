<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="flex flex-1 w-full">
      <LeftSidebar />
      <div class="p-4 flex-1">
        <h2 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-4">Quản lý công thức</h2>

        <!-- Form thêm/sửa công thức -->
        <form @submit.prevent="isEditing ? updateRecipe() : createRecipe()" class="mb-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <!-- Chọn sản phẩm -->
            <div>
              <label class="block text-gray-700 font-semibold mb-2">Sản phẩm</label>
              <select v-model="currentRecipe.product" class="w-full border p-2 rounded text-black" required>
                <option value="">-- Chọn sản phẩm --</option>
                <option v-for="product in products" :key="product.product_id" :value="product.product_id">
                  {{ product.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Danh sách nguyên liệu -->
          <h3 class="text-xl font-semibold mb-4 text-gray-800">Nguyên liệu</h3>
          <div v-for="(detail, index) in currentRecipe.details" :key="index" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4 p-4 border rounded">
            <!-- Chọn nguyên liệu -->
            <div>
              <label class="block text-gray-700 mb-2">Nguyên liệu</label>
              <select v-model="detail.ingredient" @change="updateUnitOptions(index)" class="w-full border p-2 rounded text-black" required>
                <option value="">-- Chọn nguyên liệu --</option>
                <option v-for="ingredient in ingredients" :key="ingredient.ingredient_id" :value="ingredient.ingredient_id">
                  {{ ingredient.name }}
                </option>
              </select>
            </div>

            <!-- Số lượng -->
            <div>
              <label class="block text-gray-700 mb-2">Số lượng</label>
              <input v-model.number="detail.quantity" type="number" min="1" class="w-full border p-2 rounded text-black" required />
            </div>

            <!-- Đơn vị -->
            <div>
              <label class="block text-gray-700 mb-2">Đơn vị</label>
              <select v-model="detail.unit" class="w-full border p-2 rounded text-black" required>
                <option value="">-- Chọn đơn vị --</option>
                <option v-for="unit in detail.availableUnits" :key="unit.unit_id" :value="unit.unit_id">
                  {{ unit.name }}
                </option>
              </select>
            </div>

            <!-- Nút xóa -->
            <div class="flex items-end">
              <button @click="removeIngredient(index)" type="button" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
                Xóa
              </button>
            </div>
          </div>

          <!-- Nút thêm nguyên liệu -->
          <button @click="addIngredient" type="button" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mb-6">
            Thêm nguyên liệu
          </button>

          <!-- Nút lưu/hủy -->
          <div class="flex space-x-4">
            <button type="submit" class="bg-customOrange text-white px-6 py-2 rounded font-bold hover:bg-orange-600">
              {{ isEditing ? 'Cập nhật' : 'Thêm' }} công thức
            </button>
            <button v-if="isEditing" @click="cancelEdit" type="button" class="bg-gray-500 text-white px-6 py-2 rounded hover:bg-gray-600">
              Hủy
            </button>
          </div>
        </form>

        <!-- Danh sách công thức -->
        <h2 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-4">Danh sách công thức</h2>
        
        <!-- Filter -->
        <div class="mb-4">
          <label class="block text-gray-700 font-semibold mb-2">Lọc theo sản phẩm:</label>
          <select v-model="filterProduct" class="w-full md:w-1/3 border p-2 rounded text-black">
            <option value="">Tất cả sản phẩm</option>
            <option v-for="product in products" :key="product.product_id" :value="product.product_id">
              {{ product.name }}
            </option>
          </select>
        </div>

        <div v-if="filteredRecipes.length > 0">
          <div v-for="recipe in filteredRecipes" :key="recipe.recipe_id" class="mb-8 border rounded p-4">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold text-gray-800">{{ getProductName(recipe.product) }}</h3>
              <div>
                <button @click="deleteRecipe(recipe.recipe_id)" class="text-red-500 hover:text-red-700 font-semibold">
                  Xóa
                </button>
                <button @click="editRecipe(recipe)" class="text-blue-500 hover:text-blue-700 font-semibold ml-4">
                  Sửa
                </button>
              </div>
            </div>
            
            <table class="w-full border-collapse">
              <thead>
                <tr class="bg-gray-100 text-left">
                  <th class="px-4 py-2 border">Nguyên liệu</th>
                  <th class="px-4 py-2 border">Số lượng</th>
                  <th class="px-4 py-2 border">Đơn vị</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="detail in getRecipeDetails(recipe.recipe_id)" :key="detail.recipedetail_id" class="hover:bg-gray-50">
                  <td class="px-4 py-2 border">{{ getIngredientName(detail.ingredient) }}</td>
                  <td class="px-4 py-2 border">{{ detail.quantity }}</td>
                  <td class="px-4 py-2 border">{{ getUnitName(detail.unit) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else class="text-gray-500 italic py-4">
          {{ filterProduct ? "Không tìm thấy công thức cho sản phẩm này" : "Chưa có công thức nào được tạo" }}
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
      products: [],
      ingredients: [],
      units: [],
      recipes: [],
      recipeDetails: [],
      filterProduct: "",
      isEditing: false,
      currentRecipe: {
        recipe_id: null,
        product: "",
        details: [
          {
            recipedetail_id: null,
            ingredient: "",
            quantity: 1,
            unit: "",
            availableUnits: []
          }
        ]
      }
    };
  },
  computed: {
    filteredRecipes() {
      if (!this.filterProduct) {
        return this.recipes;
      }
      return this.recipes.filter(recipe => recipe.product == this.filterProduct);
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/products/");
        this.products = res.data;
      } catch (error) {
        console.error("Lỗi khi lấy danh sách sản phẩm:", error);
      }
    },
    async fetchIngredients() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/ingredients/");
        this.ingredients = res.data;
      } catch (error) {
        console.error("Lỗi khi lấy danh sách nguyên liệu:", error);
      }
    },
    async fetchUnits() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/units/");
        this.units = res.data;
      } catch (error) {
        console.error("Lỗi khi lấy danh sách đơn vị:", error);
      }
    },
    async fetchRecipes() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/recipes/");
        this.recipes = res.data;
      } catch (error) {
        console.error("Lỗi khi lấy danh sách công thức:", error);
      }
    },
    async fetchRecipeDetails() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/recipe_details/");
        this.recipeDetails = res.data;
      } catch (error) {
        console.error("Lỗi khi lấy chi tiết công thức:", error);
      }
    },

    addIngredient() {
      this.currentRecipe.details.push({
        recipedetail_id: null,
        ingredient: "",
        quantity: 1,
        unit: "",
        availableUnits: []
      });
    },
    removeIngredient(index) {
      if (this.currentRecipe.details.length > 1) {
        this.currentRecipe.details.splice(index, 1);
      }
    },
    updateUnitOptions(index) {
      const ingredientId = this.currentRecipe.details[index].ingredient;
      const ingredient = this.ingredients.find(i => i.ingredient_id == ingredientId);
      
      if (ingredient) {
        this.currentRecipe.details[index].availableUnits = [...this.units];
        this.currentRecipe.details[index].unit = ingredient.unit;
      }
    },

    async createRecipe() {
      try {
        // Tạo recipe
        const recipeRes = await axios.post("http://127.0.0.1:8000/api/recipes/", {
          product: this.currentRecipe.product
        });

        // Tạo các recipe details
        const recipeId = recipeRes.data.recipe_id;
        await this.createRecipeDetails(recipeId);

        alert("Thêm công thức thành công!");
        this.resetForm();
        await this.fetchRecipes();
        await this.fetchRecipeDetails();
      } catch (error) {
        console.error("Lỗi khi thêm công thức:", error);
        alert("Có lỗi xảy ra khi thêm công thức!");
      }
    },
    async createRecipeDetails(recipeId) {
      for (const detail of this.currentRecipe.details) {
        await axios.post("http://127.0.0.1:8000/api/recipe_details/", {
          recipe: recipeId,
          ingredient: detail.ingredient,
          quantity: detail.quantity,
          unit: detail.unit
        });
      }
    },
    editRecipe(recipe) {
      this.isEditing = true;
      this.currentRecipe = {
        recipe_id: recipe.recipe_id,
        product: recipe.product,
        details: []
      };

      // Lấy chi tiết công thức
      const details = this.getRecipeDetails(recipe.recipe_id);
      details.forEach(detail => {
        this.currentRecipe.details.push({
          recipedetail_id: detail.recipedetail_id,
          ingredient: detail.ingredient,
          quantity: detail.quantity,
          unit: detail.unit,
          availableUnits: [...this.units]
        });
      });

      // Thêm một dòng trống nếu không có chi tiết nào
      if (this.currentRecipe.details.length === 0) {
        this.addIngredient();
      }

      // Cuộn đến form
      this.$nextTick(() => {
        const form = document.querySelector('form');
        form.scrollIntoView({ behavior: 'smooth' });
      });
    },
    async updateRecipe() {
      try {
        // Cập nhật recipe
        await axios.put(`http://127.0.0.1:8000/api/recipes/${this.currentRecipe.recipe_id}/`, {
          product: this.currentRecipe.product
        });

        // Xóa tất cả recipe details cũ
        await this.deleteRecipeDetails(this.currentRecipe.recipe_id);

        // Tạo lại các recipe details mới
        await this.createRecipeDetails(this.currentRecipe.recipe_id);

        alert("Cập nhật công thức thành công!");
        this.cancelEdit();
        await this.fetchRecipes();
        await this.fetchRecipeDetails();
      } catch (error) {
        console.error("Lỗi khi cập nhật công thức:", error);
        alert("Có lỗi xảy ra khi cập nhật công thức!");
      }
    },
    async deleteRecipeDetails(recipeId) {
      const details = this.getRecipeDetails(recipeId);
      for (const detail of details) {
        await axios.delete(`http://127.0.0.1:8000/api/recipe_details/${detail.recipedetail_id}/`);
      }
    },
    async deleteRecipe(recipeId) {
      if (!confirm("Bạn có chắc muốn xóa công thức này?")) return;
      
      try {
        await axios.delete(`http://127.0.0.1:8000/api/recipes/${recipeId}/`);
        alert("Xóa công thức thành công!");
        await this.fetchRecipes();
        await this.fetchRecipeDetails();
      } catch (error) {
        console.error("Lỗi khi xóa công thức:", error);
        alert("Có lỗi xảy ra khi xóa công thức!");
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.resetForm();
    },
    resetForm() {
      this.currentRecipe = {
        recipe_id: null,
        product: "",
        details: [
          {
            recipedetail_id: null,
            ingredient: "",
            quantity: 1,
            unit: "",
            availableUnits: []
          }
        ]
      };
    },

    getProductName(productId) {
      const product = this.products.find(p => p.product_id == productId);
      return product ? product.name : "Không xác định";
    },
    getIngredientName(ingredientId) {
      const ingredient = this.ingredients.find(i => i.ingredient_id == ingredientId);
      return ingredient ? ingredient.name : "Không xác định";
    },
    getUnitName(unitId) {
      const unit = this.units.find(u => u.unit_id == unitId);
      return unit ? unit.name : "Không xác định";
    },
    getRecipeDetails(recipeId) {
      return this.recipeDetails.filter(detail => detail.recipe == recipeId);
    }
  },
  async mounted() {
    await this.fetchProducts();
    await this.fetchIngredients();
    await this.fetchUnits();
    await this.fetchRecipes();
    await this.fetchRecipeDetails();
  }
};
</script>