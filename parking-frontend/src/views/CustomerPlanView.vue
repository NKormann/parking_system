<template>
  <v-container>
    <h1 class="text-h4 mb-5">Gerenciamento de Planos de Clientes</h1>
    <v-data-table
      :headers="headers"
      :items="customerPlans"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Planos de Clientes</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ props }">
              <v-btn color="primary" dark class="mb-2" v-bind="props">
                Novo Plano de Cliente
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-select
                        v-model="editedItem.customer_id"
                        :items="customers"
                        item-title="name"
                        item-value="id"
                        label="Cliente"
                      ></v-select>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-select
                        v-model="editedItem.plan_id"
                        :items="plans"
                        item-title="description"
                        item-value="id"
                        label="Plano"
                      ></v-select>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="editedItem.due_date"
                        label="Data de Vencimento"
                        type="date"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">Cancelar</v-btn>
                <v-btn color="blue darken-1" text @click="save">Salvar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.customer="{ item }">
        {{ item.customer.name }}
      </template>
      <template v-slot:item.plan="{ item }">
        {{ item.plan.description }}
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const dialog = ref(false)
const customerPlans = ref([])
const customers = ref([])
const plans = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  customer_id: null, 
  plan_id: null, 
  due_date: null
})
const defaultItem = {
  customer_id: null,
  plan_id: null,
  due_date: null
}

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Novo Plano de Cliente' : 'Editar Plano de Cliente'
})

const headers = [
  { title: 'Cliente', key: 'customer.name' },
  { title: 'Plano', key: 'plan.description' },
  { title: 'Data de Vencimento', key: 'due_date' },
  { title: 'Ações', key: 'actions', sortable: false }
]

async function fetchCustomerPlans() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/customerplan/')
    customerPlans.value = response.data
  } catch (error) {
    console.error('Erro ao buscar planos de clientes:', error)
  }
}

async function fetchCustomers() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/customer/')
    customers.value = response.data
  } catch (error) {
    console.error('Erro ao buscar clientes:', error)
  }
}

async function fetchPlans() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/plan/')
    plans.value = response.data
  } catch (error) {
    console.error('Erro ao buscar planos:', error)
  }
}

function editItem(item) {
  editedIndex.value = customerPlans.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  editedItem.value.customer_id = item.customer.id
  editedItem.value.plan_id = item.plan.id
  dialog.value = true
}

async function deleteItem(item) {
  const index = customerPlans.value.indexOf(item)
  if (confirm('Tem certeza que deseja deletar este plano de cliente?')) {
    try {
      await axios.delete(`http://localhost:8000/api/v1/customerplan/${item.id}/`)
      customerPlans.value.splice(index, 1)
    } catch (error) {
      console.error('Erro ao deletar plano de cliente:', error)
    }
  }
}

function close() {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem)
  editedIndex.value = -1
}

async function save() {
  try {
    if (editedIndex.value > -1) {
      await axios.put(`http://localhost:8000/api/v1/customerplan/${editedItem.value.id}/`, editedItem.value)
      Object.assign(customerPlans.value[editedIndex.value], editedItem.value)
    } else {
      const response = await axios.post('http://localhost:8000/api/v1/customerplan/', editedItem.value)
      customerPlans.value.push(response.data)
    }
    close()
  } catch (error) {
    console.error('Erro ao salvar plano de cliente:', error)
  }
}

onMounted(() => {
  fetchCustomerPlans()
  fetchCustomers()
  fetchPlans()
})
</script>
