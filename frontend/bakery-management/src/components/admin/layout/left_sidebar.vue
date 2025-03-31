<template>
    <aside class="w-64 min-h-screen bg-white shadow-lg p-4">
      <ul>
        <li v-for="(item, index) in menuItems" :key="index">
          <router-link 
            :to="item.path"
            class="flex items-center w-full p-3 rounded-lg transition-all"
            :class="$route.path === item.path
              ? 'bg-gradient-to-r from-customOrange to-customPeach text-white shadow-md font-bold font-opensans'
              : 'text-gray-700  hover:bg-gray-100 font-opensans' ">
            <component :is="item.icon" class="w-5 h-5 mr-3"/>
            {{ item.label }}
          </router-link>
        </li>
      </ul>
    </aside>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const menuItems = [
    { label: "Trang chủ", path: "/admin"},
    { label: "Danh mục sản phẩm", path: "/admin/category"},
    { label: "Sản phẩm", path: "/admin/product"},
    { label: "Nguyên liệu", path: "/admin/ingredient"},
    { label: "Công thức", path: "/admin/recipe"},
    { label: "Đơn đặt hàng", path: "/admin/order"},
    { label: "Khuyến mãi", path: "/admin/promotion"},
  ];
  </script>
  