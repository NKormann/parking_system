<template>
  <nav>
    <ul>
      <li><router-link to="/">Operação</router-link></li>
      <li><router-link to="/customers">Clientes</router-link></li>
      <li><router-link to="/vehicles">Veículos</router-link></li>
      <li><router-link to="/plans">Planos</router-link></li>
      <li><router-link to="/contracts">Contratos</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
};
</script>

<style scoped>
nav {
  background-color: #333;
}
nav ul {
  list-style: none;
  display: flex;
}
nav li {
  margin: 0 10px;
}
nav a {
  color: #fff;
  text-decoration: none;
}
</style>
