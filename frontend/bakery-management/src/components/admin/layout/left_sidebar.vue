<template>
  <aside class="w-64 min-h-screen bg-white shadow-lg p-4">
    <ul>
      <li v-for="(item, index) in menuItems" :key="index">
        <router-link 
          :to="item.path"
          class="flex items-center w-full p-3 rounded-lg transition-all"
          :class="$route.path === item.path
            ? 'bg-gradient-to-r from-customOrange to-customPeach text-white shadow-md font-bold font-opensans'
            : 'text-gray-600  hover:bg-gray-100 font-opensans' ">
          <font-awesome-icon :icon="item.icon" class="w-5 h-5 mr-3"/>
          {{ item.label }}
        </router-link>
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { faHome, faList, faBox, faFlask, faBalanceScale, faUtensils, faReceipt } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const menuItems = [
  { label: "Trang chủ", path: "/admin", icon: faHome },
  { label: "Danh mục sản phẩm", path: "/admin/category", icon: faList },
  { label: "Sản phẩm", path: "/admin/product", icon: faBox },
  { label: "Nguyên liệu", path: "/admin/ingredient", icon: faFlask },
  { label: "Đơn vị đo lường", path: "/admin/unit", icon: faBalanceScale },
  { label: "Công thức", path: "/admin/recipe", icon: faUtensils },
  { label: "Đơn hàng", path: "/admin/order", icon: faReceipt },
];

const components = {
  FontAwesomeIcon,
};
</script>

