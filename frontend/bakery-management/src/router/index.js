import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/pages/admin/dashboard.vue'
import categories from '@/pages/admin/category.vue'
import products from '@/pages/admin/product.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
   
    {
      path: '/admin',
      name: 'admin',
      component: Dashboard,
    },
    {
      path: '/admin/category',
      name: 'category',
      component: categories,
    },
    {
      path: '/admin/product',
      name: 'product',
      component: products,
    },
    
  ],
})

export default router
