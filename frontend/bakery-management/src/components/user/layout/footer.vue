<template>
  <footer class="bg-customBlack text-white py-3">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Left Section -->
        <div class="flex flex-col">
          <div class="flex items-center mb-4">
            <img src="@/assets/logo1.png" alt="Bread Icon" class="w-16 h-16 mr-2" />
            <h1 class="text-3xl font-bold font-sansita text-customPeach">Panadería</h1>
          </div>
          <p class="text-base mb-4">
            Đây là website quản lý tiệm bánh được phát triển<br />
            theo nội dung môn học Niên luận cơ sở ngành<br />
            Khoa học máy tính.
          </p>
          <div class="space-y-2">
            <p class="text-sm flex items-center">
              <font-awesome-icon :icon="['fas', 'store']" class="mr-2"/>
              Khu II, Đ. 3 Tháng 2, Xuân Khánh, Ninh Kiều, Cần Thơ
            </p>
            <p class="text-sm flex items-center">
              <font-awesome-icon :icon="['fas', 'phone']" class="mr-2" />
              +078 376 7845
            </p>
            <p class="text-sm flex items-center">
              <font-awesome-icon :icon="['fas', 'envelope']" class="mr-2"/>
              kyb2207535@student.ctu.edu.vn
            </p>
          </div>
        </div>

        <!-- Middle Section -->
        <div class="flex flex-col mt-8 ml-20">
          <h2 class="text-lg mb-4 font-semibold font-sansita text-customPeach">Khám phá</h2>
          <div class="flex flex-col space-y-2">
            <router-link to="/about" class="text-sm hover:underline">Về Panadería</router-link>
            <router-link to="/contact" class="text-sm hover:underline">Liên hệ</router-link>
            <router-link to="/products" class="text-sm hover:underline">Sản phẩm</router-link>
          </div>
        </div>

        <!-- Right Section -->
        <div class="flex flex-col mt-8">
          <h2 class="text-lg mb-4 font-semibold font-sansita text-customPeach">Theo dõi chúng tôi</h2>
          <div class="flex space-x-4">
            <a href="https://www.facebook.com" target="_blank" class="text-customPeach hover:text-customPeach">
             <i class="fa-brands fa-square-facebook" style="font-size: 2rem;"></i>
            </a>
            <a href="https://www.instagram.com/" target="_blank" class="text-customPeach hover:text-customPeach">
              <font-awesome-icon :icon="['fab', 'instagram']" class="w-8 h-8" />
            </a>
          </div>
        </div>
      </div>
      <div class="text-center text-gray-500 text-sm mt-8">
        © 2025 PANADERIA. ALL RIGHTS RESERVED.
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped>
</style>