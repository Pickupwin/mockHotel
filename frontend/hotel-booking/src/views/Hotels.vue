<template>
  <div class="hotels-page">
    <SearchBox 
      :placeholder="'Search for hotels'" 
      :initial="route.query.q as string || ''" 
      @search="onSearch" 
      @mode-change="onModeChange"
      :default-mode="(route.query.provider as string) === 'fast_start' ? 'fast' : 'normal'"
    />
    <HotelList :query="searchVal" :provider="currentProvider" />
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
// 存储当前的启动模式
const currentProvider = ref((route.query.provider as string) || 'fast_start')

// 处理模式变更
function onModeChange(provider: string) {
  currentProvider.value = provider
  // 重置搜索结果
  searchVal.value = ''
  // 更新URL参数但不刷新页面 - 只保留provider参数，移除搜索查询
  const query: any = {}
  if (provider) {
    query.provider = provider
  }
  router.replace({ query })
}

// 处理搜索事件
function onSearch(event: { value: string, provider: string }) {
  searchVal.value = event.value
  const query: any = event.value ? { q: event.value } : {}
  if (event.provider) {
    query.provider = event.provider
  }
  router.replace({ query })
}

// 监听路由参数变化
watch(() => route.query.q, (q) => { if (typeof q === 'string') searchVal.value = q })
watch(() => route.query.provider, (p) => { if (typeof p === 'string') currentProvider.value = p })
</script>
<style scoped>
.hotels-page { max-width: 900px; margin: 38px auto 0 auto; min-height: 70vh; }
</style>
