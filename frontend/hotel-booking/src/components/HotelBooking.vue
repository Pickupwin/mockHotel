<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center">
    <!-- 搜索框 -->
    <div
      class="w-full flex flex-col items-center transition-all duration-500"
      :class="{
        'mt-32': !searched,
        'mt-6': searched,
        'fixed top-0 bg-white shadow-md py-3 z-10': searched,
      }"
    >
      <div class="flex items-center w-full max-w-xl px-4">
        <input
          v-model="query"
          @keyup.enter="searchHotels"
          type="text"
          placeholder="输入目的地..."
          class="flex-1 border border-gray-300 rounded-l-xl px-4 py-2 focus:outline-none focus:ring focus:ring-blue-300"
        />
        <button
          @click="searchHotels"
          class="bg-blue-600 hover:bg-blue-700 text-white rounded-r-xl px-6 py-2"
        >
          搜索
        </button>
      </div>
    </div>

    <!-- 酒店表格 -->
    <div class="mt-24 w-full max-w-5xl px-4" v-if="searched">
      <div v-if="loading" class="text-center text-gray-500 py-10">
        正在搜索中...
      </div>
      <div v-else-if="hotels.length === 0" class="text-center text-gray-500 py-10">
        未找到相关酒店。
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200 rounded-xl shadow">
          <thead class="bg-gray-100 text-gray-700">
            <tr>
              <th class="px-4 py-3 text-left">酒店名称</th>
              <th class="px-4 py-3 text-left">品牌</th>
              <th class="px-4 py-3 text-right">价格（￥/晚）</th>
              <th class="px-4 py-3 text-center">评分</th>
              <th class="px-4 py-3 text-center">距离（km）</th>
              <th class="px-4 py-3 text-center">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="hotel in hotels"
              :key="hotel.id"
              class="border-t hover:bg-gray-50"
            >
              <td class="px-4 py-3 font-medium text-gray-900">
                {{ hotel.name }}
              </td>
              <td class="px-4 py-3 text-gray-700">
                {{ hotel.brand }}
              </td>
              <td class="px-4 py-3 text-right text-blue-700 font-semibold">
                {{ hotel.price }}
              </td>
              <td class="px-4 py-3 text-center text-yellow-600">
                {{ hotel.rating.toFixed(1) }}
              </td>
              <td class="px-4 py-3 text-center text-gray-600">
                {{ hotel.distance.toFixed(2) }}
              </td>
              <td class="px-4 py-3 text-center">
                <button
                  @click="reserveHotel(hotel)"
                  :disabled="hotel.reserved"
                  class="px-3 py-1.5 rounded-lg text-white text-sm transition"
                  :class="hotel.reserved ? 'bg-gray-400' : 'bg-green-600 hover:bg-green-700'"
                >
                  {{ hotel.reserved ? '已预定' : '预定' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 弹窗提示 -->
    <div
      v-if="popupMessage"
      class="fixed bottom-6 right-6 bg-gray-800 text-white px-4 py-2 rounded-lg shadow-lg animate-fade-in"
    >
      {{ popupMessage }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

interface Hotel {
  id: number
  name: string
  brand: string
  price: number
  rating: number
  distance: number
  reserved: boolean
}

const query = ref('')
const hotels = ref<Hotel[]>([])
const searched = ref(false)
const loading = ref(false)
const popupMessage = ref('')

async function searchHotels() {
  if (!query.value.trim()) return
  loading.value = true
  searched.value = true
  try {
    const resp = await axios.get('/hotel-search', {
      params: { location: query.value },
    })
    hotels.value = resp.data.map((h: any) => ({
      id: h.id,
      name: h.name,
      brand: h.brand,
      price: h.price,
      rating: h.rating,
      distance: h.distance,
      reserved: false,
    }))
  } catch (err) {
    console.error(err)
    showPopup('搜索失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

async function reserveHotel(hotel: Hotel) {
  try {
    const resp = await axios.post('/hotel-reserve', { hotel_id: hotel.id })
    if (resp.data.success) {
      hotel.reserved = true
      const confirmation = resp.data.confirmation || ''
      showPopup(`预订成功！确认号：${confirmation}`)
    } else {
      showPopup(resp.data.message || '预订失败，请重试')
    }
  } catch (err) {
    console.error(err)
    showPopup('预订失败，请检查网络连接')
  }
}

function showPopup(msg: string) {
  popupMessage.value = msg
  setTimeout(() => (popupMessage.value = ''), 2500)
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>
