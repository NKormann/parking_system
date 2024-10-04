<template>
    <v-container>
      <v-toolbar flat color="primary">
        <v-toolbar-title class="white--text">Cadastro de Contratos</v-toolbar-title>
      </v-toolbar>
  
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
          v-model="contract.description"
          label="Descrição"
          :rules="[rules.required]"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="contract.max_value"
          label="Valor Máximo"
          type="number"
        ></v-text-field>
  
        <v-btn color="success" @click="saveContract">Salvar</v-btn>
      </v-form>
  
      <v-divider class="my-4"></v-divider>
  
      <v-btn color="primary" @click="addRule">Adicionar Regra</v-btn>
  
      <v-data-table
        :headers="ruleHeaders"
        :items="contractRules"
        item-key="id"
        @click:row="editRule"
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
        contract: {
          description: '',
          max_value: '',
        },
        contractRules: [],
        ruleHeaders: [
          { text: 'Até (minutos)', value: 'until' },
          { text: 'Valor', value: 'value' },
        ],
        rules: {
          required: (value) => !!value || 'Campo obrigatório',
        },
      };
    },
    methods: {
      saveContract() {
        if (this.$refs.form.validate()) {
          if (this.contract.id) {
            api
              .put(`contract/${this.contract.id}/`, this.contract)
              .then(() => {
                alert('Contrato atualizado com sucesso');
              })
              .catch((error) => {
                alert(error.response.data.error || 'Erro ao salvar contrato');
              });
          } else {
            api
              .post('contract/', this.contract)
              .then((response) => {
                this.contract = response.data;
                alert('Contrato salvo com sucesso');
              })
              .catch((error) => {
                alert(error.response.data.error || 'Erro ao salvar contrato');
              });
          }
        }
      },
      fetchContractRules() {
        if (this.contract.id) {
          api
            .get('contractrule/', { params: { contract: this.contract.id } })
            .then((response) => {
              this.contractRules = response.data;
            })
            .catch((error) => {
              console.error(error);
            });
        }
      },
      addRule() {
        const until = prompt('Até (minutos):');
        const value = prompt('Valor:');
  
        if (until && value) {
          api
            .post('contractrule/', {
              contract: this.contract.id,
              until: parseInt(until),
              value: parseFloat(value),
            })
            .then(() => {
              this.fetchContractRules();
            })
            .catch((error) => {
              alert(error.response.data.error || 'Erro ao adicionar regra');
            });
        }
      },
      editRule(item) {
        // Implementar edição de regra se necessário
      },
    },
    created() {
      // Buscar o primeiro contrato ou iniciar um novo
      api
        .get('contract/')
        .then((response) => {
          if (response.data.length > 0) {
            this.contract = response.data[0];
            this.fetchContractRules();
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  };
  </script>
  