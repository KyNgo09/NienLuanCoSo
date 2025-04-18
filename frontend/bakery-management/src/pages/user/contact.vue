<template>
    <div class="min-h-screen flex flex-col">
      <Header />
      <main class="flex-grow">
        <!-- Hero Banner -->
        <div class="relative h-96 overflow-hidden">
        <img 
          src="@/assets/contact-banner.png" 
          alt="Liên hệ Panadería" 
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
          <div class="text-center px-4">
            <h1 class="text-4xl md:text-5xl font-bold text-customPeach mb-4 font-sansita">Liên Hệ Với Panadería</h1>
            <p class="text-xl text-white max-w-2xl mx-auto">
              Cùng chia sẻ niềm đam mê ẩm thực với chúng tôi
            </p>
          </div>
        </div>
      </div>
        <!-- Contact Content -->
        <div class="container mx-auto px-4 py-16">
          <div class="max-w-6xl mx-auto">
            <!-- Contact Cards -->
            <div class="grid md:grid-cols-3 gap-8 mb-16">
              <div class="bg-white p-8 rounded-xl shadow-md text-center border-t-4 border-customOrange">
                <div class="text-amber-600 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-2">Điện Thoại</h3>
                <p class="text-gray-600 mb-2">Zalo: 0783 767 845</p>
                <p class="text-gray-600">Đặt bánh: 0783 767 845</p>
              </div>
  
              <div class="bg-white p-8 rounded-xl shadow-md text-center border-t-4 border-customOrange">
                <div class="text-amber-600 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-2">Email</h3>
                <p class="text-gray-600 mb-2">CSKH: kydaingo@gmail.com</p>
                <p class="text-gray-600">Hợp tác: kyb2207535@student.ctu.edu.vn</p>
              </div>
  
              <div class="bg-white p-8 rounded-xl shadow-md text-center border-t-4 border-customOrange">
                <div class="text-amber-600 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-2">Địa Chỉ</h3>
                <p class="text-gray-600">Khu II, Đ. 3 Tháng 2, Xuân Khánh</p>
                <p class="text-gray-600">Ninh Kiều, Cần Thơ</p>
              </div>
            </div>
  
            <!-- Contact Form & Map -->
            <div class="grid md:grid-cols-2 gap-12 items-start">
              <!-- Contact Form -->
              <div class="bg-white p-8 rounded-xl shadow-md">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Gửi Tin Nhắn Cho Chúng Tôi</h2>
                <form @submit.prevent="submitForm" class="space-y-4">
                  <div>
                    <label for="name" class="block text-gray-700 mb-2">Họ và tên</label>
                    <input 
                      type="text" 
                      id="name" 
                      v-model="form.name"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-amber-500 focus:border-amber-500"
                      required
                    >
                  </div>
                  <div>
                    <label for="email" class="block text-gray-700 mb-2">Email</label>
                    <input 
                      type="email" 
                      id="email" 
                      v-model="form.email"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-amber-500 focus:border-amber-500"
                      required
                    >
                  </div>
                  <div>
                    <label for="phone" class="block text-gray-700 mb-2">Số điện thoại</label>
                    <input 
                      type="tel" 
                      id="phone" 
                      v-model="form.phone"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-amber-500 focus:border-amber-500"
                    >
                  </div>
                  <div>
                    <label for="message" class="block text-gray-700 mb-2">Nội dung</label>
                    <textarea 
                      id="message" 
                      v-model="form.message"
                      rows="4"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-amber-500 focus:border-amber-500"
                      required
                    ></textarea>
                  </div>
                  <button 
                    type="submit" 
                    class="w-full bg-customOrange text-white py-3 px-6 rounded-lg hover:bg-orange-600 transition duration-300"
                  >
                    Gửi Tin Nhắn
                  </button>
                </form>
              </div>
  
              <!-- Map & Hours -->
              <div>
                <div class="bg-white p-6 rounded-xl shadow-md mb-8">
                  <h3 class="text-xl font-bold text-gray-800 mb-4">Giờ Mở Cửa</h3>
                  <ul class="space-y-3">
                    <li class="flex justify-between border-b pb-2">
                      <span class="text-gray-700">Thứ 2 - Thứ 6</span>
                      <span class="font-medium">7:00 - 21:00</span>
                    </li>
                    <li class="flex justify-between border-b pb-2">
                      <span class="text-gray-700">Thứ 7</span>
                      <span class="font-medium">7:00 - 22:00</span>
                    </li>
                    <li class="flex justify-between">
                      <span class="text-gray-700">Chủ Nhật</span>
                      <span class="font-medium">8:00 - 20:00</span>
                    </li>
                  </ul>
                </div>
  
                <div class="bg-gray-200 rounded-xl overflow-hidden shadow-md aspect-w-16 aspect-h-9">
                  <!-- Embedded Google Map -->
                  <iframe 
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3928.715876484774!2d105.7680403147941!3d10.03093339283056!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31a0883d6163d8a7%3A0x3b9fa2a0b91e3a4c!2zVHLGsOG7nW5nIMSQ4bqhaSBI4buNYyBD4bqnbiBUaMah!5e0!3m2!1svi!2s!4v1620000000000!5m2!1svi!2s" 
                    width="100%" 
                    height="300" 
                    style="border:0;" 
                    allowfullscreen="" 
                    loading="lazy"
                    class="rounded-xl"
                  ></iframe>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  </template>
  
  <script>
  import Header from "@/components/user/layout/header.vue";
  import Footer from "@/components/user/layout/footer.vue";
  
  export default {
    name: 'ContactPage',
    components: {
      Header,
      Footer,
    },
    data() {
      return {
        form: {
          name: '',
          email: '',
          phone: '',
          message: ''
        }
      }
    },
    methods: {
      submitForm() {
        // Xử lý gửi form ở đây
        console.log('Form submitted:', this.form);
        alert('Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể.');
        this.resetForm();
      },
      resetForm() {
        this.form = {
          name: '',
          email: '',
          phone: '',
          message: ''
        }
      }
    },
    metaInfo() {
      return {
        title: 'Liên Hệ - Panadería',
        meta: [
          { name: 'description', content: 'Liên hệ với tiệm bánh Panadería - Chuyên các loại bánh ngọt, bánh mì và bánh truyền thống chất lượng cao' }
        ]
      }
    }
  }
  </script>
  
  