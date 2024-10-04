<!-- src/components/Customer.vue -->

<template>
  <div>
    <h1>Clientes</h1>
    <div>
      <label>Nome:</label>
      <input v-model="customer.name" placeholder="Nome" />
    </div>
    <div>
      <label>Cartão ID:</label>
      <input v-model="customer.card_id" placeholder="Cartão ID" />
    </div>
    <button @click="saveCustomer">{{ isEditing ? 'Atualizar' : 'Salvar' }}</button>
    <h2>Lista de Clientes</h2>
    <table>
      <thead>
        <tr>
          <th>Nome</th>
          <th>Cartão ID</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cust in customers" :key="cust.id">
          <td>{{ cust.name }}</td>
          <td>{{ cust.card_id }}</td>
          <td>
            <button @click="editCustomer(cust)">Editar</button>
            <button @click="deleteCustomer(cust.id)">Excluir</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  data() {
    return {
      customer: {
        name: '',
        card_id: '',
      },
      customers: [],
      isEditing: false,
    };
  },
  methods: {
    fetchCustomers() {
      api.get('customer/').then((response) => {
        this.customers = response.data;
      });
    },
    saveCustomer() {
      if (this.isEditing) {
        api
          .put(`customer/${this.customer.id}/`, this.customer)
          .then(() => {
            this.resetForm();
            this.fetchCustomers();
          })
          .catch((error) => {
            alert(error.response.data.error);
          });
      } else {
        api
          .post('customer/', this.customer)
          .then(() => {
            this.resetForm();
            this.fetchCustomers();
          })
          .catch((error) => {
            alert(error.response.data.error);
          });
      }
    },
    editCustomer(cust) {
      this.customer = { ...cust };
      this.isEditing = true;
    },
    deleteCustomer(id) {
      api.delete(`customer/${id}/`).then(() => {
        this.fetchCustomers();
      });
    },
    resetForm() {
      this.customer = {
        name: '',
        card_id: '',
      };
      this.isEditing = false;
    },
  },
  created() {
    this.fetchCustomers();
  },
};
</script>

<style scoped>
/* Estilos específicos */
</style>
