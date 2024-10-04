<template>
  <v-container>
    <h1 class="text-h4 mb-5">Gerenciamento de Movimentos de Estacionamento</h1>
    <v-data-table
      :headers="headers"
      :items="parkMovements"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Movimentos de Estacionamento</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ props }">
              <v-btn color="primary" dark class="mb-2" v-bind="props">
                Novo Movimento
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
                      <v-text-field
                        v-model="editedItem.plate"
                        label="Placa do Veículo"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="editedItem.card_id"
                        label="Card ID do Cliente"
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
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="exitVehicle(item)">mdi-exit-run</v-icon>
        <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
      <template v-slot:item.value="{ item }">
        R$ {{ item.value ? item.value.toFixed(2) : '-' }}
      </template>
      <template v-slot:item.entry_date="{ item }">
        {{ new Date(item.entry_date).toLocaleString() }}
      </template>
      <template v-slot:item.exit_date="{ item }">
        {{ item.exit_date ? new Date(item.exit_date).toLocaleString() : '-' }}
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const dialog = ref(false)
const parkMovements = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  plate: '',
  card_id: ''
})
const defaultItem = {
  plate: '',
  card_id: ''
}

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Novo Movimento' : 'Editar Movimento'
})

const headers = [
  { title: 'Placa', key: 'vehicle_plate' },
  { title: 'Entrada', key: 'entry_date' },
  { title: 'Saída', key: 'exit_date' },
  { title: 'Valor', key: 'value' },
  { title: 'Ações', key: 'actions', sortable: false }
]

async function fetchParkMovements() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/parkmovement/')
    parkMovements.value = response.data
  } catch (error) {
    console.error('Erro ao buscar movimentos de estacionamento:', error)
  }
}

async function save() {
  try {
    if (!editedItem.value.plate && !editedItem.value.card_id) {
      alert('Por favor, forneça a Placa do veículo ou o Card ID do cliente.')
      return
    }
    
    // Se for uma nova entrada, verifica se existe um veículo e cliente associado à placa ou card_id.
    const response = await axios.post('http://localhost:8000/api/v1/parkmovement/', {
      plate: editedItem.value.plate || null,
      card_id: editedItem.value.card_id || null
    })
    
    parkMovements.value.push(response.data)
    close()
  } catch (error) {
    console.error('Erro ao registrar movimento de entrada:', error)
  }
}

async function exitVehicle(item) {
  try {
    const response = await axios.post(`http://localhost:8000/api/v1/parkmovement/${item.id}/exit/`)
    const index = parkMovements.value.indexOf(item)
    parkMovements.value[index] = response.data
  } catch (error) {
    console.error('Erro ao registrar saída do veículo:', error)
  }
}

async function deleteItem(item) {
  const index = parkMovements.value.indexOf(item)
  if (confirm('Tem certeza que deseja deletar este movimento?')) {
    try {
      await axios.delete(`http://localhost:8000/api/v1/parkmovement/${item.id}/`)
      parkMovements.value.splice(index, 1)
    } catch (error) {
      console.error('Erro ao deletar movimento de estacionamento:', error)
    }
  }
}

function close() {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem)
  editedIndex.value = -1
}

onMounted(fetchParkMovements)
</script>
