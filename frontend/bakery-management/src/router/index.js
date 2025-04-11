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

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Admin routes
    {
      path: '/admin',
      component: Admin,
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
        { path: '', name: 'home', component: Home},
        {path: 'products', name: 'products', component: User_Product},
        {path: 'account', name: 'account', component: Account},
      ],
    },
  ],
})

export default router
