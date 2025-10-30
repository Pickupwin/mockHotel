<template>
  <div class="hotels-page">
    <SearchBox :placeholder="'Search for hotels'" :initial="route.query.q as string || ''" @search="onSearch" />
    <HotelList :query="searchVal" />
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SearchBox from '../components/SearchBox.vue'
import HotelList from '../components/HotelList.vue'
const route = useRoute()
const router = useRouter()
const searchVal = ref((route.query.q as string) || '')
function onSearch(val: string) {
  searchVal.value = val
  router.replace({ path: '/hotels', query: val ? { q: val } : {} })
}
watch(() => route.query.q, (q) => { if (typeof q === 'string') searchVal.value = q })
</script>
<style scoped>
.hotels-page { max-width: 900px; margin: 38px auto 0 auto; min-height: 70vh; }
</style>
