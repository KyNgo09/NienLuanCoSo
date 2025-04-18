<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    <main class="flex-grow">
      <!-- Hero Banner -->
      <section class="relative h-screen min-h-[500px] flex items-center">
        <!-- Background Image -->
        <div class="absolute inset-0 overflow-hidden">
          <img src="@/assets/home-banner.png" alt="Background Panadería" class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-black bg-opacity-30"></div>
        </div>

        <!-- Content Container -->
        <div class="container mx-auto px-4 z-10 relative">
          <div class="grid md:grid-cols-2 gap-8 items-center">
            <!-- Text Content -->
            <div class="text-center md:text-left text-white">
              <h2 class="text-3xl md:text-5xl lg:text-6xl font-bold mb-4 drop-shadow-md font-sansita">
                Hương vị ngọt ngào,
              </h2>
              <h2 class="text-3xl md:text-5xl lg:text-6xl font-bold mb-10 drop-shadow-md font-sansita">
                Món ngon hoàn hảo!
              </h2>
              <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
                <router-link to="/products"
                  class="bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 shadow-lg transform hover:scale-105">
                  Mua Ngay
                </router-link>
                <router-link to="/about"
                  class="bg-white bg-opacity-90 hover:bg-opacity-100 text-amber-600 font-bold py-3 px-6 rounded-lg transition duration-300 shadow-lg transform hover:scale-105">
                  Khám Phá
                </router-link>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- Featured Products -->
      <section class="py-16 bg-white">
        <div class="container mx-auto px-4">
          <h2 class="text-4xl font-bold text-center text-customBrown mb-12 font-sansita">Sản Phẩm Nổi Bật</h2>
          <div class="grid md:grid-cols-3 gap-8">
            <div v-for="(product, index) in featuredProducts" :key="index"
              class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow">
              <img :src="product.image" :alt="product.name" class="w-full h-64 object-cover" />
              <div class="p-6">
                <h3 class="text-xl font-bold text-gray-800 mb-2">{{ product.name }}</h3>
                <p class="text-customOrange font-bold text-lg mb-4">{{ product.price }}</p>
                <p class="text-gray-600 mb-4">{{ product.description }}</p>
                <router-link to="/products" class="text-amber-600 font-medium hover:underline">
                  Xem chi tiết →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Why Choose Us -->
      <section class="py-16 bg-amber-50">
        <div class="container mx-auto px-4">
          <h2 class="text-3xl font-bold text-center text-customBrown font-sansita mb-12">Tại Sao Chọn Panadería ?</h2>
          <div class="grid md:grid-cols-3 gap-8">
            <div class="text-center p-6">
              <div
                class="text-amber-600 mb-4 mx-auto w-16 h-16 flex items-center justify-center rounded-full bg-amber-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-2">Chất Lượng Đảm Bảo</h3>
              <p class="text-gray-600">Nguyên liệu tự nhiên, không chất bảo quản, đạt chuẩn vệ sinh an toàn thực phẩm
              </p>
            </div>
            <div class="text-center p-6">
              <div
                class="text-amber-600 mb-4 mx-auto w-16 h-16 flex items-center justify-center rounded-full bg-amber-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-2">Giao Hàng Nhanh</h3>
              <p class="text-gray-600">Giao hàng tận nơi trong vòng 2h tại nội thành, đảm bảo bánh tươi ngon nhất</p>
            </div>
            <div class="text-center p-6">
              <div
                class="text-amber-600 mb-4 mx-auto w-16 h-16 flex items-center justify-center rounded-full bg-amber-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-2">Giá Cả Hợp Lý</h3>
              <p class="text-gray-600">Nhiều ưu đãi hấp dẫn, giá cả cạnh tranh với chất lượng vượt trội</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Customer Reviews -->
      <section class="py-16 bg-white">
        <div class="container mx-auto px-4">
          <h2 class="text-4xl font-bold text-center text-customBrown font-sansita mb-12">Đánh Giá Từ Khách Hàng</h2>
          <div class="grid md:grid-cols-3 gap-8">
            <div v-for="(review, index) in customerReviews" :key="index"
              class="bg-white p-6 rounded-xl shadow-md border border-gray-100">
              <div class="flex items-center mb-4">
                <div class="flex items-center text-amber-400 mr-2">
                  <svg v-for="star in 5" :key="star" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5"
                    :class="{ 'text-gray-300': star > review.rating }" viewBox="0 0 20 20" fill="currentColor">
                    <path
                      d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
                <span class="text-gray-500 text-sm">{{ review.date }}</span>
              </div>
              <p class="text-gray-700 mb-4 italic">"{{ review.comment }}"</p>
              <div class="flex items-center">
                <img :src="review.avatar" :alt="review.name" class="w-10 h-10 rounded-full mr-3" />
                <div>
                  <h4 class="font-bold text-gray-800">{{ review.name }}</h4>
                  <p class="text-gray-500 text-sm">{{ review.role }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

    </main>
    <Footer />
  </div>
</template>

<script>
import Header from "@/components/user/layout/header.vue";
import Footer from "@/components/user/layout/footer.vue";
import banhMiImage from '@/assets/banh-sd.png';
import banhNgotImage from '@/assets/banh-ngot.png';
import banhTtImage from '@/assets/banh-dalon.png';
import userAvatar from '@/assets/user.png';
export default {
  name: 'HomePage',
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      featuredProducts: [
        {
          name: 'Bánh Mì Sourdough',
          price: '35.000 ₫',
          description: 'Bánh mì chua tự nhiên với lớp vỏ giòn tan, ruột mềm dai',
          image: banhMiImage
        },
        {
          name: 'Bánh Tiramisu',
          price: '65.000 ₫',
          description: 'Hương vị Ý đích thực với lớp mascarpone mềm mịn',
          image: banhNgotImage
        },
        {
          name: 'Bánh Da Lợn',
          price: '25.000 ₫',
          description: 'Bánh truyền thống với lớp lá dứa thơm ngon đặc trưng',
          image: banhTtImage
        }
      ],
      customerReviews: [
        {
          name: 'Chị Ngọc Anh',
          role: 'Khách hàng thân thiết',
          comment: 'Bánh ở Panadería ngon tuyệt vời! Tôi đã mua ở đây 3 năm liền và chưa bao giờ thất vọng.',
          rating: 5,
          date: '12/05/2023',
          avatar: userAvatar
        },
        {
          name: 'Anh Minh Đức',
          role: 'Food Blogger',
          comment: 'Chất lượng bánh vượt xa mong đợi với mức giá hợp lý. Đặc biệt thích bánh mì sourdough ở đây!',
          rating: 4,
          date: '28/04/2023',
          avatar: userAvatar
        },
        {
          name: 'Chị Thanh Hương',
          role: 'Nhân viên văn phòng',
          comment: 'Dịch vụ giao hàng nhanh, bánh luôn tươi ngon. Nhân viên rất thân thiện và nhiệt tình.',
          rating: 5,
          date: '05/05/2023',
          avatar: userAvatar
        }
      ]
    }
  },
}

</script>

