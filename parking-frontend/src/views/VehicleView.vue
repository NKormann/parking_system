<template>
  <v-container>
    <h1 class="text-h4 mb-5">Gerenciamento de Veículos</h1>
    <v-data-table
      :headers="headers"
      :items="vehicles"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Veículos</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ props }">
              <v-btn color="primary" dark class="mb-2" v-bind="props">
                Novo Veículo
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.plate" label="Placa"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.model" label="Modelo"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.description" label="Descrição"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-select
                        v-model="editedItem.customer_id"
                        :items="customers"
                        item-title="name"
                        item-value="id"
                        label="Cliente"
                      ></v-select>
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
        {{ item.customer ? item.customer.name : 'Rotativo' }}
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
const vehicles = ref([])
const customers = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  plate: '',
  model: '',
  description: '',
  customer_id: null
})
const defaultItem = {
  plate: '',
  model: '',
  description: '',
  customer_id: null
}

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Novo Veículo' : 'Editar Veículo'
})

const headers = [
  { title: 'Placa', key: 'plate' },
  { title: 'Modelo', key: 'model' },
  { title: 'Descrição', key: 'description' },
  { title: 'Cliente', key: 'customer' },
  { title: 'Ações', key: 'actions', sortable: false }
]

async function fetchVehicles() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/vehicle/')
    vehicles.value = response.data
  } catch (error) {
    console.error('Erro ao buscar veículos:', error)
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

function editItem(item) {
  editedIndex.value = vehicles.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  editedItem.value.customer_id = item.customer ? item.customer.id : null
  dialog.value = true
}

async function deleteItem(item) {
  const index = vehicles.value.indexOf(item)
  if (confirm('Tem certeza que deseja deletar este veículo?')) {
    try {
      await axios.delete(`http://localhost:8000/api/v1/vehicle/${item.id}/`)
      vehicles.value.splice(index, 1)
    } catch (error) {
      console.error('Erro ao deletar veículo:', error)
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
      await axios.put(`http://localhost:8000/api/v1/vehicle/${editedItem.value.id}/`, editedItem.value)
      Object.assign(vehicles.value[editedIndex.value], editedItem.value)
    } else {
      const response = await axios.post('http://localhost:8000/api/v1/vehicle/', editedItem.value)
      vehicles.value.push(response.data)
    }
    close()
  } catch (error) {
    console.error('Erro ao salvar veículo:', error)
  }
}

onMounted(() => {
  fetchVehicles()
  fetchCustomers()
})
</script>
