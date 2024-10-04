import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/customers',
    name: 'Customers',
    component: () => import('@/views/CustomerView.vue')
  },
  {
    path: '/vehicles',
    name: 'Vehicles',
    component: () => import('@/views/VehicleView.vue')
  },
  {
    path: '/plans',
    name: 'Plans',
    component: () => import('@/views/PlanView.vue')
  },
  {
    path: '/customer-plans',
    name: 'CustomerPlans',
    component: () => import('@/views/CustomerPlanView.vue')
  },
  {
    path: '/contracts',
    name: 'Contracts',
    component: () => import('@/views/ContractView.vue')
  },
  {
    path: '/contract-rules',
    name: 'ContractRules',
    component: () => import('@/views/ContractRuleView.vue')
  },
  {
    path: '/park-movements',
    name: 'ParkMovements',
    component: () => import('@/views/ParkMovementView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router