<!-- src/components/Contract.vue -->

<template>
  <div>
    <h1>Contratos</h1>
    <div>
      <label>Descrição:</label>
      <input v-model="contract.description" placeholder="Descrição" />
    </div>
    <div>
      <label>Valor Máximo:</label>
      <input v-model="contract.max_value" placeholder="Valor Máximo" type="number" />
    </div>
    <h2>Regras do Contrato</h2>
    <div v-for="(rule, index) in contractRules" :key="index">
      <label>Até (minutos):</label>
      <input v-model="rule.until" type="number" />
      <label>Valor:</label>
      <input v-model="rule.value" type="number" />
      <button @click="removeRule(index)">Remover</button>
    </div>
    <button @click="addRule">Adicionar Regra</button>
    <button @click="saveContract">{{ isEditing ? 'Atualizar' : 'Salvar' }}</button>
    <h2>Lista de Contratos</h2>
    <table>
      <thead>
        <tr>
          <th>Descrição</th>
          <th>Valor Máximo</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cont in contracts" :key="cont.id">
          <td>{{ cont.description }}</td>
          <td>{{ cont.max_value }}</td>
          <td>
            <button @click="editContract(cont)">Editar</button>
            <button @click="deleteContract(cont.id)">Excluir</button>
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
      contract: {
        description: '',
        max_value: '',
      },
      contractRules: [],
      contracts: [],
      isEditing: false,
    };
  },
  methods: {
    fetchContracts() {
      api.get('contract/').then((response) => {
        this.contracts = response.data;
      });
    },
    saveContract() {
      const contractData = { ...this.contract };
      contractData.contract_rules = this.contractRules;

      if (this.isEditing) {
        api.put(`contract/${this.contract.id}/`, contractData).then(() => {
          this.resetForm();
          this.fetchContracts();
        });
      } else {
        api.post('contract/', contractData).then(() => {
          this.resetForm();
          this.fetchContracts();
        });
      }
    },
    editContract(cont) {
      this.contract = { ...cont };
      // Obter as regras do contrato
      api.get(`contractrule/?contract=${cont.id}`).then((response) => {
        this.contractRules = response.data;
      });
      this.isEditing = true;
    },
    deleteContract(id) {
      api.delete(`contract/${id}/`).then(() => {
        this.fetchContracts();
      });
    },
    addRule() {
      this.contractRules.push({ until: '', value: '' });
    },
    removeRule(index) {
      this.contractRules.splice(index, 1);
    },
    resetForm() {
      this.contract = {
        description: '',
        max_value: '',
      };
      this.contractRules = [];
      this.isEditing = false;
    },
  },
  created() {
    this.fetchContracts();
  },
};
</script>

<style scoped>
/* Estilos específicos */
</style>
