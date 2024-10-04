<template>
    <v-container>
      <v-toolbar flat color="primary">
        <v-toolbar-title class="white--text">Cadastro de Veículos</v-toolbar-title>
      </v-toolbar>
  
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
          v-model="vehicle.plate"
          label="Placa"
          :rules="[rules.required]"
          required
        ></v-text-field>
  
        <v-text-field v-model="vehicle.model" label="Modelo"></v-text-field>
        <v-text-field v-model="vehicle.description" label="Descrição"></v-text-field>
  
        <v-select
          v-model="vehicle.customer"
          :items="customers"
          item-text="name"
          item-value="id"
          label="Cliente"
          return-object
        ></v-select>
  
        <v-btn color="success" @click="saveVehicle">Salvar</v-btn>
      </v-form>
  
      <v-data-table
        :headers="headers"
        :items="vehicles"
        item-key="id"
        @click:row="editVehicle"
        class="elevation-1"
      >
        <template v-slot:item.customer="{ item }">
          {{ item.customer ? item.customer.name : 'Rotativo' }}
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
        vehicle: {
          plate: '',
          model: '',
          description: '',
          customer: null,
        },
        vehicles: [],
        customers: [],
        headers: [
          { text: 'Placa', value: 'plate' },
          { text: 'Modelo', value: 'model' },
          { text: 'Cliente', value: 'customer' },
        ],
        rules: {
          required: (value) => !!value || 'Campo obrigatório',
        },
      };
    },
    methods: {
      fetchVehicles() {
        api
          .get('vehicle/')
          .then((response) => {
            this.vehicles = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      fetchCustomers() {
        api
          .get('customer/')
          .then((response) => {
            this.customers = response.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      saveVehicle() {
        if (this.$refs.form.validate()) {
          const data = { ...this.vehicle };
          data.customer = data.customer ? data.customer.id : null;
  
          if (this.vehicle.id) {
            api
              .put(`vehicle/${this.vehicle.id}/`, data)
              .then(() => {
                this.fetchVehicles();
                this.resetForm();
              })
              .catch((error) => {
                alert(error.response.data.error || 'Erro ao salvar veículo');
              });
          } else {
            api
              .post('vehicle/', data)
              .then(() => {
                this.fetchVehicles();
                this.resetForm();
              })
              .catch((error) => {
                alert(error.response.data.error || 'Erro ao salvar veículo');
              });
          }
        }
      },
      editVehicle(item) {
        this.vehicle = { ...item, customer: item.customer || null };
      },
      resetForm() {
        this.vehicle = {
          plate: '',
          model: '',
          description: '',
          customer: null,
        };
        this.$refs.form.reset();
      },
    },
    created() {
      this.fetchVehicles();
      this.fetchCustomers();
    },
  };
  </script>
  