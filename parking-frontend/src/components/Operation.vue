<!-- src/components/Operation.vue -->

<template>
  <div>
    <h1>Operação do Estacionamento</h1>
    <div>
      <label>Placa:</label>
      <input v-model="plate" placeholder="Placa" />
    </div>
    <div>
      <label>Valor a cobrar:</label>
      <input v-model="amount" placeholder="Valor a cobrar" disabled />
    </div>
    <div>
      <button @click="enterVehicle">Entrada</button>
      <button @click="exitVehicle" :disabled="!selectedMovement">Saída</button>
    </div>
    <h2>Veículos no Pátio</h2>
    <table>
      <thead>
        <tr>
          <th>Data de Entrada</th>
          <th>Placa</th>
          <th>Cartão</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="movement in movements"
          :key="movement.id"
          @click="selectMovement(movement)"
          :class="{ selected: movement.id === selectedMovement?.id }"
        >
          <td>{{ movement.entry_date }}</td>
          <td>{{ movement.vehicle.plate }}</td>
          <td>{{ movement.vehicle.customer?.card_id || 'N/A' }}</td>
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
      plate: '',
      amount: '',
      movements: [],
      selectedMovement: null,
    };
  },
  methods: {
    fetchMovements() {
      api
        .get('parkmovement/', {
          params: { exit_date__isnull: 'true' },
        })
        .then((response) => {
          this.movements = response.data;
        });
    },
    enterVehicle() {
      api
        .post('parkmovement/', { plate: this.plate })
        .then(() => {
          this.plate = '';
          this.fetchMovements();
        })
        .catch((error) => {
          alert(error.response.data.error);
        });
    },
    selectMovement(movement) {
      this.selectedMovement = movement;
      this.amount = movement.value || '';
    },
    exitVehicle() {
      api
        .put(`parkmovement/${this.selectedMovement.id}/`, {})
        .then((response) => {
          this.amount = response.data.value;
          this.selectedMovement = null;
          this.fetchMovements();
        })
        .catch((error) => {
          alert(error.response.data.error);
        });
    },
  },
  created() {
    this.fetchMovements();
  },
};
</script>

<style scoped>
.selected {
  background-color: #f0f0f0;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 8px;
  border: 1px solid #ddd;
}
</style>
