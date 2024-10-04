<template>
    <v-container>
      <h1 class="text-h3 mb-5">Bem-vindo ao Sistema de Gerenciamento de Estacionamento</h1>
      <v-row>
        <v-col v-for="item in menuItems" :key="item.title" cols="12" sm="6" md="4">
          <v-card :to="item.path" link>
            <v-card-title>
              <v-icon left>{{ item.icon }}</v-icon>
              {{ item.title }}
            </v-card-title>
            <v-card-text>{{ item.description }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const menuItems = ref([
    { title: 'Clientes', path: '/customers', icon: 'mdi-account', description: 'Gerenciar cadastro de clientes' },
    { title: 'Veículos', path: '/vehicles', icon: 'mdi-car', description: 'Gerenciar cadastro de veículos' },
    { title: 'Planos', path: '/plans', icon: 'mdi-clipboard-list', description: 'Gerenciar planos de estacionamento' },
    { title: 'Planos de Clientes', path: '/customer-plans', icon: 'mdi-account-cash', description: 'Associar planos a clientes' },
    { title: 'Contratos', path: '/contracts', icon: 'mdi-file-document', description: 'Gerenciar contratos' },
    { title: 'Regras de Contrato', path: '/contract-rules', icon: 'mdi-ruler', description: 'Definir regras de contrato' },
    { title: 'Movimentações', path: '/park-movements', icon: 'mdi-garage', description: 'Registrar entradas e saídas de veículos' },
  ])
  </script>