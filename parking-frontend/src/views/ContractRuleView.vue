<template>
    <v-container>
      <h1 class="text-h4 mb-5">Gerenciamento de Regras de Contrato</h1>
      <v-data-table
        :headers="headers"
        :items="contractRules"
        :items-per-page="5"
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Regras de Contrato</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ props }">
                <v-btn color="primary" dark class="mb-2" v-bind="props">
                  Nova Regra de Contrato
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
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.until"
                          label="Até (minutos)"
                          type="number"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.value"
                          label="Valor"
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
        <template v-slot:item.value="{ item }">
          R$ {{ item.value.toFixed(2) }}
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import axios from 'axios'
  
  const dialog = ref(false)
  const contractRules = ref([])
  const contracts = ref([])
  const editedIndex = ref(-1)
  const editedItem = ref({
    contract: null,
    until: null,
    value: 0
  })
  const defaultItem = {
    contract: null,
    until: null,
    value: 0
  }
  
  const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'Nova Regra de Contrato' : 'Editar Regra de Contrato'
  })
  
  const headers = [
    { title: 'Até (minutos)', key: 'until' },
    { title: 'Valor', key: 'value' },
    { title: 'Ações', key: 'actions', sortable: false }
  ]
  
  async function fetchContractRules() {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/contractrule/')
      contractRules.value = response.data
    } catch (error) {
      console.error('Erro ao buscar regras de contrato:', error)
    }
  }
  
  async function fetchContracts() {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/contract/')
      contracts.value = response.data
    } catch (error) {
      console.error('Erro ao buscar contratos:', error)
    }
  }
  
  function editItem(item) {
    editedIndex.value = contractRules.value.indexOf(item)
    editedItem.value = Object.assign({}, item)
    dialog.value = true
  }
  
  async function deleteItem(item) {
    const index = contractRules.value.indexOf(item)
    if (confirm('Tem certeza que deseja deletar esta regra de contrato?')) {
      try {
        await axios.delete(`http://localhost:8000/api/v1/contractrule/${item.id}/`)
        contractRules.value.splice(index, 1)
      } catch (error) {
        console.error('Erro ao deletar regra de contrato:', error)
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
        await axios.put(`http://localhost:8000/api/v1/contractrule/${editedItem.value.id}/`, editedItem.value)
        Object.assign(contractRules.value[editedIndex.value], editedItem.value)
      } else {
        const response = await axios.post('http://localhost:8000/api/v1/contractrule/', editedItem.value)
        contractRules.value.push(response.data)
      }
      close()
    } catch (error) {
      console.error('Erro ao salvar regra de contrato:', error)
    }
  }
  
  onMounted(() => {
    fetchContractRules()
    fetchContracts()
  })
  </script>
  