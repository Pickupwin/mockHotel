<template>
  <NavBar />
  <main style="padding-top: 64px"><router-view /></main>
</template>
<script setup lang="ts">
import NavBar from './components/NavBar.vue'
</script>
<style>
body {
  margin: 0;
  font-family: 'Inter', 'Helvetica', sans-serif;
  background-color: #f9fafb;
}
</style>
