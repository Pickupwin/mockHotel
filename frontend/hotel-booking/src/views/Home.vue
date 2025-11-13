<template>
  <div class="home-page">
    <section class="intro-section">
      <h1 class="headline">Find Your Perfect Stay</h1>
      <SearchBox 
        :placeholder="'Where do you want to go?'" 
        @search="onSearch"
      />
    </section>
    <RoomPreview />
  </div>
</template>
<script setup lang="ts">
import { useRouter } from 'vue-router'
import SearchBox from '../components/SearchBox.vue'
import RoomPreview from '../components/RoomPreview.vue'

const router = useRouter()
// 处理搜索事件
function onSearch(event: { value: string, provider?: string }) {
  if (event.value) {
    router.push({
      path: '/hotels', 
      query: { 
        q: event.value,
        provider: event.provider 
      } 
    })
  }
}
</script>
<style scoped>
.home-page { min-height: calc(100vh - 70px); }
.headline {
  text-align: center;
  font-size: 2.2rem;
  font-weight: 700;
  color: #23377b;
  margin-top: 24px;
  letter-spacing: 1px;
  margin-bottom: 20px;
}
.intro-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
}
</style>
