<template>
    <v-navigation-drawer app>
      <v-list>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const menuItems = ref([
    { title: 'Início', path: '/', icon: 'mdi-home' },
    { title: 'Clientes', path: '/customers', icon: 'mdi-account' },
    { title: 'Veículos', path: '/vehicles', icon: 'mdi-car' },
    { title: 'Planos', path: '/plans', icon: 'mdi-clipboard-list' },
    { title: 'Planos de Clientes', path: '/customer-plans', icon: 'mdi-account-cash' },
    { title: 'Contratos', path: '/contracts', icon: 'mdi-file-document' },
    { title: 'Regras de Contrato', path: '/contract-rules', icon: 'mdi-ruler' },
    { title: 'Movimentações', path: '/park-movements', icon: 'mdi-garage' },
  ])
  </script>