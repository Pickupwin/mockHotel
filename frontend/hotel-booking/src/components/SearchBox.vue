<template>
  <form class="search-form" @submit.prevent="onSubmit">
    <input type="text" v-model="search" :placeholder="placeholder" />
    <button type="submit">Search</button>
  </form>
</template>
<script setup lang="ts">
import { defineEmits, ref } from 'vue'
const emit = defineEmits(['search'])
const props = defineProps<{ placeholder?: string, initial?: string }>()
const search = ref(props.initial || '')
function onSubmit() {
  emit('search', search.value.trim())
}
</script>
<style scoped>
.search-form {
  width: 100%;
  max-width: 500px;
  display: flex;
  gap: 9px;
  margin: 0 auto;
}
.search-form input {
  flex: 1;
  font-size: 1.08rem;
  padding: 13px 18px;
  border: 1px solid #dde2ea;
  border-radius: 12px;
  background: #fff;
  transition: border-color 0.18s;
}
.search-form input:focus {
  border-color: #337eff;
}
.search-form button {
  background: #337eff;
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  padding: 13px 22px;
  cursor: pointer;
  font-size: 1.05rem;
}
.search-form button:hover { background: #1a4ddb; }
</style>
