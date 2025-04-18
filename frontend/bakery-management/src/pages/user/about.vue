<template>
    <div class="min-h-screen flex flex-col">
      <Header />
      <main class="flex-grow">
        <!-- Banner Section -->
        <div class="relative h-96 overflow-hidden">
          <img 
            src="@/assets/about-banner.png" 
            alt="Panadería Bakery" 
            class="w-full h-full object-cover"
          />
          <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
            <h1 class="text-5xl font-bold text-customPeach text-center font-sansita ">Về Panadería</h1>
          </div>
        </div>
  
        <!-- About Content -->
        <div class="container mx-auto px-4 py-12">
          <section class="max-w-4xl mx-auto">
            <div class="mb-12">
              <h2 class="text-3xl font-bold text-gray-800 mb-6">Câu Chuyện Của Chúng Tôi</h2>
              <div class="grid md:grid-cols-2 gap-8 items-center">
                <div>
                  <p class="text-lg text-gray-600 mb-4">
                    Panadería được thành lập từ những năm 90 với niềm đam mê bất tận dành cho nghệ thuật làm bánh. 
                    Từ một cửa hàng trong con hẻm nhỏ, chúng tôi đã phát triển thành thương hiệu bánh uy tín 
                    được hàng nghìn khách hàng yêu mến.
                  </p>
                  <p class="text-lg text-gray-600">
                    Chúng tôi tin rằng mỗi chiếc bánh không chỉ là món ăn mà còn là tác phẩm nghệ thuật, 
                    chứa đựng tình yêu và sự sáng tạo của người làm bánh.
                  </p>
                </div>
                <img 
                  src="@/assets/logo1.png" 
                  alt="Our Story" 
                  class="rounded-lg shadow-lg"
                />
              </div>
            </div>
  
            <div class="mb-12">
              <h2 class="text-3xl font-bold text-gray-800 mb-6">Triết Lý Của Panadería</h2>
              <div class="bg-amber-50 p-8 rounded-lg">
                <p class="text-xl italic text-amber-800 mb-4">
                  "Nguyên liệu chất lượng - Công thức hoàn hảo - Tình yêu đích thực"
                </p>
                <ul class="space-y-4 text-gray-700">
                  <li class="flex items-start">
                    <span class="text-amber-600 mr-2">✓</span>
                    <span>Chỉ sử dụng nguyên liệu tự nhiên, không chất bảo quản</span>
                  </li>
                  <li class="flex items-start">
                    <span class="text-amber-600 mr-2">✓</span>
                    <span>Kết hợp tinh hoa ẩm thực truyền thống và hiện đại</span>
                  </li>
                  <li class="flex items-start">
                    <span class="text-amber-600 mr-2">✓</span>
                    <span>Mỗi sản phẩm là một trải nghiệm vị giác độc đáo</span>
                  </li>
                </ul>
              </div>
            </div>
  
            <div class="mb-12">
              <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Sản Phẩm Nổi Bật</h2>
              <div class="grid md:grid-cols-3 gap-6">
                <div class="bg-white p-6 rounded-lg shadow-md text-center">
                  <img 
                    src="@/assets/banh-mi.png" 
                    alt="Bánh mì" 
                    class="h-48 w-full object-cover rounded mb-4"
                  />
                  <h3 class="text-xl font-semibold text-gray-800 mb-2">Bánh Tươi</h3>
                  <p class="text-gray-600">Giòn tan vỏ ngoài, mềm mịn bên trong với hương thơm đặc trưng</p>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md text-center">
                  <img 
                    src="@/assets/banh-ngot.png" 
                    alt="Bánh ngọt" 
                    class="h-48 w-full object-cover rounded mb-4"
                  />
                  <h3 class="text-xl font-semibold text-gray-800 mb-2">Bánh Ngọt</h3>
                  <p class="text-gray-600">Tinh tế từ hình thức đến hương vị, hoàn hảo cho mọi dịp</p>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md text-center">
                  <img 
                    src="@/assets/banh-tt.png" 
                    alt="Bánh truyền thống" 
                    class="h-48 w-full object-cover rounded mb-4"
                  />
                  <h3 class="text-xl font-semibold text-gray-800 mb-2">Bánh Truyền Thống</h3>
                  <p class="text-gray-600">Giữ trọn hương vị quê nhà với công thức gia truyền</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  </template>
  
  <script>
  import Header from "@/components/user/layout/header.vue";
  import Footer from "@/components/user/layout/footer.vue";
  
  export default {
    name: 'AboutPage',
    components: {
      Header,
      Footer,
    },
    metaInfo() {
      return {
        title: 'Về Chúng Tôi - Panadería',
        meta: [
          { name: 'description', content: 'Giới thiệu về tiệm bánh Panadería - Chuyên các loại bánh ngọt, bánh mì và bánh truyền thống chất lượng cao' }
        ]
      }
    }
  }
  </script>
  
  <style scoped>
  /* Custom styles can be added here */
  </style>