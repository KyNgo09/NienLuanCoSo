import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/pages/admin/dashboard.vue'
import category from '@/pages/admin/category.vue'
import product from '@/pages/admin/product.vue'
import ingredient from '@/pages/admin/ingredient.vue'
import recipe from '@/pages/admin/recipe.vue'
import order from '@/pages/admin/order.vue'
import promotion from '@/pages/admin/promotion.vue'
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
      component: category,
    },
    {
      path: '/admin/product',
      name: 'product',
      component: product,
    },
    {
      path: '/admin/ingredient',
      name: 'ingredient',
      component: ingredient,
    },
    {
      path: '/admin/recipe',
      name: 'recipe',
      component: recipe,
    },
    {
      path: '/admin/order',
      name: 'order',
      component: order,
    },
    {
      path: '/admin/promotion',
      name: 'promotion',
      component: promotion,
    },
  ],
})

export default router
