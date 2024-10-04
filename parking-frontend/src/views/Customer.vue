<template>
    <v-container>
      <v-toolbar flat color="primary">
        <v-toolbar-title class="white--text">Cadastro de Clientes</v-toolbar-title>
      </v-toolbar>
  
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
          v-model="customer.name"
          label="Nome"
          :rules="[rules.required]"
          required
        ></v-text-field>
  
        <v-text-field v-model="customer.card_id" label="ID do Cartão"></v-text-field>
  
        <v-btn color="success" @click="saveCustomer">Salvar</v-btn>
      </v-form>
  
      <v-data-table
        :headers="headers"
        :items="customers"
        item-key="id"
        @click:row="editCustomer"
        class="elevation-1"
      ></v-data-table>
    </v-container>
  </template>
  
  <script>
  import api from '@/services/api';
  
  export default {
    data() {
      return {
        valid: true,
        customer: {
          name: '',
          card_id: '',
        },
        customers: [],
        headers: [
          { text: 'Nome', value: 'name' },
          { text: 'ID do Cartão', value: 'card_id' },
        ],
        rules: {
          required: (value) => !!value || 'Campo obrigatório',
        },
      };
    },
    methods: {
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
      saveCustomer() {
        if (this.$refs.form.validate()) {
          if (this.customer.id) {
            api
              .put(`customer/${this.customer.id}/`, this.customer)
              .then(() => {
                this.fetchCustomers();
                this.resetForm();
              })
              .catch((error) => {
                alert(error.response.data.error || 'Erro ao salvar cliente');
              });
          } else {
            api
              .post('customer/', this.customer)
              .then(() => {
                this.fetchCustomers();
                this.resetForm();
              })
              .catch((error) => {
                alert(error.response.data.error || 'Erro ao salvar cliente');
              });
          }
        }
      },
      editCustomer(item) {
        this.customer = { ...item };
      },
      resetForm() {
        this.customer = {
          name: '',
          card_id: '',
        };
        this.$refs.form.reset();
      },
    },
    created() {
      this.fetchCustomers();
    },
  };
  </script>
  