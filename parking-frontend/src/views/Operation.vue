<template>
    <v-container>
      <v-toolbar flat color="primary">
        <v-toolbar-title class="white--text">Operação do Estacionamento</v-toolbar-title>
      </v-toolbar>
  
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
          v-model="plate"
          label="Placa"
          :rules="[rules.required]"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="amount"
          label="Valor a cobrar"
          disabled
        ></v-text-field>
  
        <v-btn color="success" @click="enterVehicle">Entrada</v-btn>
        <v-btn
          color="error"
          @click="exitVehicle"
          :disabled="!selectedMovement"
        >
          Saída
        </v-btn>
      </v-form>
  
      <v-data-table
        :headers="headers"
        :items="movements"
        item-key="id"
        @click:row="selectMovement"
        class="elevation-1"
      >
        <template v-slot:item.customer="{ item }">
          {{ item.vehicle.customer ? item.vehicle.customer.name : 'Rotativo' }}
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script>
  import api from '@/services/api';
  
  export default {
    data() {
      return {
        valid: true,
        plate: '',
        amount: '',
        movements: [],
        selectedMovement: null,
        headers: [
          { text: 'Data de Entrada', value: 'entry_date' },
          { text: 'Placa', value: 'vehicle.plate' },
          { text: 'Cliente', value: 'customer' },
        ],
        rules: {
          required: (value) => !!value || 'Campo obrigatório',
        },
      };
    },
    methods: {
      fetchMovements() {
        api
          .get('parkmovement/', { params: { exit_date__isnull: 'true' } })
          .then((response) => {
            this.movements = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      enterVehicle() {
        if (this.$refs.form.validate()) {
          api
            .post('parkmovement/', { plate: this.plate })
            .then(() => {
              this.fetchMovements();
              this.plate = '';
            })
            .catch((error) => {
              alert(error.response.data.error || 'Erro ao dar entrada');
            });
        }
      },
      selectMovement(item) {
        this.selectedMovement = item;
        this.amount = item.value || '';
      },
      exitVehicle() {
        if (this.selectedMovement) {
          api
            .put(`parkmovement/${this.selectedMovement.id}/`, {
              exit_date: new Date().toISOString(),
            })
            .then((response) => {
              this.amount = response.data.value;
              this.fetchMovements();
              this.selectedMovement = null;
            })
            .catch((error) => {
              alert(error.response.data.error || 'Erro ao dar saída');
            });
        }
      },
    },
    created() {
      this.fetchMovements();
    },
  };
  </script>
  
  <style scoped>
  .v-toolbar {
    margin-bottom: 20px;
  }
  </style>
  