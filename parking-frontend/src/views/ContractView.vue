<template>
  <v-container>
    <h1 class="text-h4 mb-5">Gerenciamento de Contratos</h1>
    <v-data-table
      :headers="headers"
      :items="contracts"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Contratos</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ props }">
              <v-btn color="primary" dark class="mb-2" v-bind="props">
                Novo Contrato
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="8">
                      <v-text-field v-model="editedItem.description" label="Descrição"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.max_value"
                        label="Valor Máximo"
                        prefix="R$"
                        type="number"
                        step="0.01"
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
        <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
      <template v-slot:item.max_value="{ item }">
        R$ {{ item.max_value ? item.max_value.toFixed(2) : '-' }}
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const dialog = ref(false)
const contracts = ref([])
const editedIndex = ref(-1)
const editedItem = ref({
  description: '',
  max_value: null
})
const defaultItem = {
  description: '',
  max_value: null
}

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'Novo Contrato' : 'Editar Contrato'
})

const headers = [
  { title: 'Descrição', key: 'description' },
  { title: 'Valor Máximo', key: 'max_value' },
  { title: 'Ações', key: 'actions', sortable: false }
]

async function fetchContracts() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/contract/')
    contracts.value = response.data
  } catch (error) {
    console.error('Erro ao buscar contratos:', error)
  }
}

function editItem(item) {
  editedIndex.value = contracts.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

async function deleteItem(item) {
  const index = contracts.value.indexOf(item)
  if (confirm('Tem certeza que deseja deletar este contrato?')) {
    try {
      await axios.delete(`http://localhost:8000/api/v1/contract/${item.id}/`)
      contracts.value.splice(index, 1)
    } catch (error) {
      console.error('Erro ao deletar contrato:', error)
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
      await axios.put(`http://localhost:8000/api/v1/contract/${editedItem.value.id}/`, editedItem.value)
      Object.assign(contracts.value[editedIndex.value], editedItem.value)
    } else {
      const response = await axios.post('http://localhost:8000/api/v1/contract/', editedItem.value)
      contracts.value.push(response.data)
    }
    close()
  } catch (error) {
    console.error('Erro ao salvar contrato:', error)
  }
}

onMounted(fetchContracts)
</script>