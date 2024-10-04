import Vue from 'vue';
import VueRouter from 'vue-router';

import Operation from '@/views/Operation.vue';
import Vehicle from '@/views/Vehicle.vue';
import Customer from '@/views/Customer.vue';
import Plan from '@/views/Plan.vue';
import Contract from '@/views/Contract.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Operation',
    component: Operation,
  },
  {
    path: '/vehicles',
    name: 'Vehicle',
    component: Vehicle,
  },
  {
    path: '/customers',
    name: 'Customer',
    component: Customer,
  },
  {
    path: '/plans',
    name: 'Plan',
    component: Plan,
  },
  {
    path: '/contracts',
    name: 'Contract',
    component: Contract,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
