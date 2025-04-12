<template>
    <footer class="bg-customBlack text-white py-8">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between items-start">
          <!-- Left Section -->
          <div class="mb-6 md:mb-0">
            <div class="flex items-center mb-4">
              <!-- Thay placeholder bằng thẻ img -->
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
                <i class="fa-solid fa-store mr-2"></i>
                Khu II, Đ. 3 Tháng 2, Xuân Khánh, Ninh Kiều, Cần Thơ
              </p>
              <p class="text-sm flex items-center">
                <i class="fa-solid fa-phone mr-2"></i>
                +078 376 7845
              </p>
              <p class="text-sm flex items-center">
                <i class="fa-solid fa-envelope mr-2"></i>
                kyb2207535@student.ctu.edu.vn
              </p>
            </div>
          </div>
  
          <!-- Right Section -->
          <div class="flex flex-col ">
            <div class="flex space-x-4 mb-4">
              <a href="#" class="text-white hover:text-gray-300">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.04c-5.5 0-10 4.5-10 10 0 4.41 3.66 8.11 8.44 9.47.62.12.82-.27.82-.6v-2.17c-3.34.72-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.74.08-.73.08-.73 1.21.09 1.85 1.24 1.85 1.24.72 1.24 1.89 1.24 3.17.95 0 2.23-.81 2.73-1.58 2.88.12.34.48 1.02.48 2.06v3.04c0 .33.21.72.81.6A10 10 0 0022 12.04c0-5.5-4.5-10-10-10zm-1.5 15.3c-.22.07-.45-.07-.52-.3-.07-.22.07-.45.3-.52.22-.07.45.07.52.3.07.22-.07.45-.3.52zm1.5 0c-.22.07-.45-.07-.52-.3-.07-.22.07-.45.3-.52.22-.07.45.07.52.3.07.22-.07.45-.3.52zm2.5-.5c-.2.14-.48.02-.62-.17-.14-.2-.02-.48.17-.62.2-.14.48-.02.62.17.14.2.02.48-.17.62zm2-.5c-.16.18-.44.14-.62-.03-.18-.16-.14-.44.03-.62.16-.18.44-.14.62.03.18.16.14.44-.03.62zm1.5-1c-.09.22-.34.32-.56.23-.22-.09-.32-.34-.23-.56.09-.22.34-.32.56-.23.22.09.32.34.23.56zm1.5-1c-.02.24-.24.4-.48.38-.24-.02-.4-.24-.38-.48.02-.24.24-.4.48-.38.24.02.4.24.38.48z"/>
                </svg>
              </a>
              <a href="#" class="text-white hover:text-gray-300">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 16h-2v-2h2v2zm0-4h-2v-6h2v6zm-5 4h-2v-2h2v2zm0-4h-2v-6h2v6zm-5 4h-2v-2h2v2zm0-4h-2v-6h2v6z"/>
                </svg>
              </a>
            </div>
            <div class="text-right">
  <h2 class="text-lg mb-4 font-semibold font-sansita text-customPeach">Khám phá</h2>
  <div class="flex flex-col">
    <router-link to="/about" class="text-sm hover:underline">Về Panaderia</router-link>
    <router-link to="/contact" class="text-sm hover:underline">Liên hệ</router-link>
    <router-link to="/products" class="text-sm hover:underline">Sản phẩm</router-link>
  </div>
</div>
          </div>
        </div>
        <div class="text-center text-gray-500 text-sm mt-6">
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
  /* Nếu cần thêm style bổ sung */
  </style>