import { createRouter, createWebHistory } from 'vue-router'

// Layouts
import Admin from '@/layouts/admin.vue'
import User from '@/layouts/user.vue' 

// Admin pages
import Dashboard from '@/pages/admin/dashboard.vue'
import Category from '@/pages/admin/category.vue'
import Product from '@/pages/admin/product.vue'
import Ingredient from '@/pages/admin/ingredient.vue'
import Recipe from '@/pages/admin/recipe.vue'
import Order from '@/pages/admin/order.vue'
import Promotion from '@/pages/admin/promotion.vue'
import Unit from '@/pages/admin/unit.vue'

// User pages
import User_Product from '@/pages/user/product.vue'
import Home from '@/pages/user/home.vue'
import Account from '@/pages/user/account.vue'
import ProductDetail from '@/pages/user/product_detail.vue'
import Cart from '@/pages/user/cart.vue'
import About from '@/pages/user/about.vue'
import Checkout from '@/pages/user/checkout.vue'
import Contact from '@/pages/user/contact.vue'
import RecentOrder from '@/pages/user/recent_order.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Admin routes
    {
      path: '/admin/',
      component: Admin,
      meta: { requiresAdmin: true }, // Đánh dấu route yêu cầu quyền admin
      children: [
        { path: '', name: 'admin', component: Dashboard },
        { path: 'category', name: 'category', component: Category },
        { path: 'product', name: 'product', component: Product },
        { path: 'ingredient', name: 'ingredient', component: Ingredient },
        { path: 'recipe', name: 'recipe', component: Recipe },
        { path: 'order', name: 'order', component: Order },
        { path: 'promotion', name: 'promotion', component: Promotion },
        { path: 'unit', name: 'unit', component: Unit },
      ],
    },
    // User routes
    {
      path: '/',
      component: User,
      children: [
        { path: '', name: 'home', component: Home },
        { path: 'products', name: 'products', component: User_Product },
        { path: 'account', name: 'account', component: Account },
        { path: '/product/:id', name: 'ProductDetail', component: ProductDetail },
        { path: 'cart', name: 'cart', component: Cart },
        { path: 'checkout', name: 'checkout', component: Checkout },
        { path: 'about', name: 'about', component: About },
        { path: 'contact', name: 'contact', component: Contact },
        { path: 'recent_orders', name: 'recent_orders', component: RecentOrder },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAdmin) {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.email === 'admin@panaderia.com') {
      next();
    } else {
      alert('Bạn không phải Admin hoặc chưa đăng nhập vào tài khoản của Admin!')
      next('/'); 
    }
  } else {
    next(); 
  }
});

export default router
