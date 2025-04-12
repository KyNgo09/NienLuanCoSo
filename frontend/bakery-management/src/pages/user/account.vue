<template>
  <div class="flex flex-col min-h-screen w-full">
    <Header />
    <div class="min-h-screen flex items-center justify-center bg-gray-100 py-12">
      <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <!-- Form Đăng nhập -->
        <div v-if="showLoginForm">
          <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Đăng nhập</h2>
          <form @submit.prevent="handleLogin">
            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-semibold mb-2" for="login-email">Email</label>
              <input v-model="loginForm.email" type="email" id="login-email"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập email của bạn" required />
            </div>
            <div class="mb-6">
              <label class="block text-gray-700 text-sm font-semibold mb-2" for="login-password">Mật khẩu</label>
              <input v-model="loginForm.password" type="password" id="login-password"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập mật khẩu" required />
            </div>
            <button type="submit"
              class="w-full bg-customOrange text-white py-2 rounded-lg hover:bg-orange-500 transition duration-200">
              Đăng nhập
            </button>
            <p v-if="loginError" class="mt-4 text-red-500 text-center">{{ loginError }}</p>
            <p v-if="loginSuccess" class="mt-4 text-green-500 text-center">{{ loginSuccess }}</p>
            <p class="mt-4 text-center">
              Chưa có tài khoản?
              <span @click="showLoginForm = false" class="text-blue-500 underline cursor-pointer hover:text-blue-600">
                Đăng ký
              </span>
            </p>
          </form>
        </div>

        <!-- Form Đăng ký -->
        <div v-else>
          <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Đăng ký</h2>
          <form @submit.prevent="handleRegister">
            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-semibold mb-2" for="register-email">Email</label>
              <input v-model="registerForm.email" type="email" id="register-email"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập email của bạn" required />
            </div>
            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-semibold mb-2" for="register-password">Mật khẩu</label>
              <input v-model="registerForm.password" type="password" id="register-password"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập mật khẩu" required />
            </div>
            <div class="mb-4">
              <label class="block text-gray-700 text-sm font-semibold mb-2" for="confirm-password">Nhập lại mật
                khẩu</label>
              <input v-model="registerForm.confirmPassword" type="password" id="confirm-password"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập lại mật khẩu" required />
            </div>
            <div class="mb-6">
              <label class="block text-gray-700 text-sm font-semibold mb-2" for="username">Tên người dùng</label>
              <input v-model="registerForm.username" type="text" id="username"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập tên người dùng" />
            </div>
            <button type="submit"
              class="w-full bg-customOrange text-white py-2 rounded-lg hover:bg-orange-500 transition duration-200">
              Đăng ký
            </button>
            <p v-if="registerError" class="mt-4 text-red-500 text-center">{{ registerError }}</p>
            <p v-if="registerSuccess" class="mt-4 text-green-500 text-center">{{ registerSuccess }}</p>
            <p class="mt-4 text-center">
              Đã có tài khoản?
              <span @click="showLoginForm = true" class="text-blue-500 underline cursor-pointer hover:text-blue-600">
                Đăng nhập
              </span>
            </p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/user/layout/header.vue";
import axios from 'axios';

export default {
  components: {
    Header,
  },
  data() {
    return {
      showLoginForm: true,
      loginForm: {
        email: '',
        password: '',
      },
      registerForm: {
        email: '',
        password: '',
        confirmPassword: '',
        username: '',
      },
      loginError: '',
      loginSuccess: '',
      registerError: '',
      registerSuccess: '',
      userId: null,  // Lưu user_id sau đăng nhập
    };
  },
  methods: {
    async handleLogin() {
      try {
        console.log('Login sending:', this.loginForm);
        const response = await axios.post('http://localhost:8000/api/login/', this.loginForm);
        this.loginSuccess = response.data.message;
        this.loginError = '';
        console.log('Login response:', response.data);

        // Lưu user_id, user, customer
        localStorage.setItem('user_id', response.data.user.id);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        localStorage.setItem('customer', JSON.stringify(response.data.customer || null));
        this.$emit('login-success'); // Thêm event để thông báo Header
        window.location.href = 'http://localhost:5173/';
      } catch (error) {
        console.error('Login error:', error.response);
        this.loginError = error.response?.data?.message || 'Đăng nhập thất bại';
        this.loginSuccess = '';
      }
    },
    async handleRegister() {
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.registerError = 'Mật khẩu không khớp';
        this.registerSuccess = '';
        return;
      }
      try {
        console.log('Register sending:', {
          email: this.registerForm.email,
          password: this.registerForm.password,
          username: this.registerForm.username
        });
        const response = await axios.post('http://localhost:8000/api/register/', {
          email: this.registerForm.email,
          password: this.registerForm.password,
          username: this.registerForm.username,
        });
        this.registerSuccess = response.data.message;
        this.registerError = '';
        console.log('Register response:', response.data);
        setTimeout(() => {
          this.registerForm = { email: '', password: '', confirmPassword: '', username: '' };
          this.registerSuccess = '';
          this.showLoginForm = true;
        }, 2000);
      } catch (error) {
        console.error('Register error:', error.response);
        this.registerError = error.response?.data?.message || 'Đăng ký thất bại';
        this.registerSuccess = '';
      }
    },
  },
};
</script>