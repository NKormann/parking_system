<!-- src/components/Vehicle.vue -->

<template>
  <div>
    <h1>Veículos</h1>
    <div>
      <label>Placa:</label>
      <input v-model="vehicle.plate" placeholder="Placa" />
    </div>
    <div>
      <label>Modelo:</label>
      <input v-model="vehicle.model" placeholder="Modelo" />
    </div>
    <div>
      <label>Descrição:</label>
      <input v-model="vehicle.description" placeholder="Descrição" />
    </div>
    <div>
      <label>Cliente:</label>
      <select v-model="vehicle.customer">
        <option :value="null">Nenhum</option>
        <option v-for="cust in customers" :key="cust.id" :value="cust.id">
          {{ cust.name }}
        </option>
      </select>
    </div>
    <button @click="saveVehicle">{{ isEditing ? 'Atualizar' : 'Salvar' }}</button>
    <h2>Lista de Veículos</h2>
    <table>
      <thead>
        <tr>
          <th>Placa</th>
          <th>Modelo</th>
          <th>Descrição</th>
          <th>Cliente</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="veh in vehicles" :key="veh.id">
          <td>{{ veh.plate }}</td>
          <td>{{ veh.model }}</td>
          <td>{{ veh.description }}</td>
          <td>{{ veh.customer_name || 'N/A' }}</td>
          <td>
            <button @click="editVehicle(veh)">Editar</button>
            <button @click="deleteVehicle(veh.id)">Excluir</button>
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
      vehicle: {
        plate: '',
        model: '',
        description: '',
        customer: null,
      },
      vehicles: [],
      customers: [],
      isEditing: false,
    };
  },
  methods: {
    fetchVehicles() {
      api.get('vehicle/').then((response) => {
        this.vehicles = response.data.map((veh) => ({
          ...veh,
          customer_name: veh.customer ? this.customers.find((c) => c.id === veh.customer)?.name : null,
        }));
      });
    },
    fetchCustomers() {
      api.get('customer/').then((response) => {
        this.customers = response.data;
        this.fetchVehicles();
      });
    },
    saveVehicle() {
      if (this.isEditing) {
        api
          .put(`vehicle/${this.vehicle.id}/`, this.vehicle)
          .then(() => {
            this.resetForm();
            this.fetchVehicles();
          })
          .catch((error) => {
            alert(error.response.data.error);
          });
      } else {
        api
          .post('vehicle/', this.vehicle)
          .then(() => {
            this.resetForm();
            this.fetchVehicles();
          })
          .catch((error) => {
            alert(error.response.data.error);
          });
      }
    },
    editVehicle(veh) {
      this.vehicle = { ...veh };
      this.isEditing = true;
    },
    deleteVehicle(id) {
      api.delete(`vehicle/${id}/`).then(() => {
        this.fetchVehicles();
      });
    },
    resetForm() {
      this.vehicle = {
        plate: '',
        model: '',
        description: '',
        customer: null,
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
