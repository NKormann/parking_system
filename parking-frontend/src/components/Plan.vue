<!-- src/components/Plan.vue -->

<template>
  <div>
    <h1>Planos</h1>
    <div>
      <label>Descrição:</label>
      <input v-model="plan.description" placeholder="Descrição" />
    </div>
    <div>
      <label>Valor:</label>
      <input v-model="plan.value" placeholder="Valor" type="number" />
    </div>
    <button @click="savePlan">{{ isEditing ? 'Atualizar' : 'Salvar' }}</button>
    <h2>Lista de Planos</h2>
    <table>
      <thead>
        <tr>
          <th>Descrição</th>
          <th>Valor</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pln in plans" :key="pln.id">
          <td>{{ pln.description }}</td>
          <td>{{ pln.value }}</td>
          <td>
            <button @click="editPlan(pln)">Editar</button>
            <button @click="deletePlan(pln.id)">Excluir</button>
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
      plan: {
        description: '',
        value: '',
      },
      plans: [],
      isEditing: false,
    };
  },
  methods: {
    fetchPlans() {
      api.get('plan/').then((response) => {
        this.plans = response.data;
      });
    },
    savePlan() {
      if (this.isEditing) {
        api.put(`plan/${this.plan.id}/`, this.plan).then(() => {
          this.resetForm();
          this.fetchPlans();
        });
      } else {
        api.post('plan/', this.plan).then(() => {
          this.resetForm();
          this.fetchPlans();
        });
      }
    },
    editPlan(pln) {
      this.plan = { ...pln };
      this.isEditing = true;
    },
    deletePlan(id) {
      api.delete(`plan/${id}/`).then(() => {
        this.fetchPlans();
      });
    },
    resetForm() {
      this.plan = {
        description: '',
        value: '',
      };
      this.isEditing = false;
    },
  },
  created() {
    this.fetchPlans();
  },
};
</script>

<style scoped>
/* Estilos específicos */
</style>
