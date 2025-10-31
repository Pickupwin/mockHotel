<template>
  <div class="results">
    <div v-if="!query" class="empty-hint">Enter a search to see available hotels...</div>
    <div v-else>
      <div v-if="loading" class="hint">Searching...</div>
      <div v-else-if="hotels.length === 0" class="hint">No hotels found.</div>
      <div v-else class="table-wrap">
        <table class="hotel-table">
          <thead>
            <tr>
              <th>酒店</th>
              <th class="right">价格（元/晚）</th>
              <th class="center">评分</th>
              <th class="center">预定</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="hotel in hotels" :key="hotel.name" :class="{ 'zebra': $index % 2 === 1 }">
              <td>
                <span class="hotel-name">{{ hotel.name }}</span>
              </td>
              <td class="right">¥{{ hotel.price.toFixed(2) }}</td>
              <td class="center"><span class="rating-star">★</span>{{ hotel.rating.toFixed(1) }}</td>
              <td class="center">
                <button
                  class="book-btn"
                  @click="book(hotel)"
                  :disabled="hotel.booked"
                  :class="hotel.booked ? 'booked' : ''"
                >
                  {{ hotel.booked ? '预定成功' : '预定' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <transition name="success-fade">
      <div v-if="popupMessage" class="reservation-toast">{{ popupMessage }}</div>
    </transition>
  </div>
</template>
<script lang="ts" setup>
import { ref, watch } from 'vue'
const props = defineProps<{ query: string }>()
interface HotelItem {
  name: string
  price: number
  rating: number
  booked?: boolean
}
const hotels = ref<HotelItem[]>([])
const loading = ref(false)
const popupMessage = ref('')

import { ftInvoke } from '../api/ftInvoke'

async function fetchHotels(query: string) {
  if (!query) { hotels.value = []; return }
  loading.value = true
  try {
    const resp = await ftInvoke({
      app_id: 13,
      path: '/root/sbw/mockHotel/backend/Hotel-DSL',
      name: "hotel"
    })
    console.log('Response from ftInvoke:', resp.data)


    
    // 硬编码的响应数据
    const retval = {
      'hotelsearch01': {
        status: 'Ok',
        data: {
          points: [
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [11.005425938142121, 20.15904998047844], 'value': 79.34284414975781},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [9.760065447306577, 22.716869007218076], 'value': 73.26373347519274},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [12.342473222449968, 22.321929696014553], 'value': 70.4982983824738},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [7.408477610539155, 22.058459373193717], 'value': 46.984229202369754},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [6.024882106569196, 19.065888540728803], 'value': 77.166834861537},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [10.053130612931604, 15.3799278505507], 'value': 82.73747215278824},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [15.108092100766711, 20.473399286501405], 'value': 72.57983997782196},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [15.886876842182552, 19.72491917778273], 'value': 26.558865994159888},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [13.296712090357499, 15.013577190813532], 'value': 92.57094721099838},
            {'brand': 'd3cab088-a6d3-4522-b07f-9b46baf2afb5', 'coords': [8.162750327878598, 13.319991305086287], 'value': 95.85538040075944}
          ]
        }
      }
    }

    // 品牌列表
    const brands = ["汉庭", "希尔顿", "如家", "假日", "7天", "全季", "晋江", "万豪", "港丽", "凯悦"]
    // 修饰列表
    const diffs = ["南口", "东门", "北门", "西街", "东街", "南门", "西门", "北口", "东口", "西口", "南街", "北街"]

    
    // 从响应数据中生成酒店列表
    const points = retval.hotelsearch01.data.points
    const list = points.map((point, index) => {
      // 随机选择品牌
      const randomBrand = brands[Math.floor(Math.random() * brands.length)]
      // 生成酒店名称
      const name = `${randomBrand}酒店（${query}${diffs[index]}店）`
      // 将value转换为五分制评分（假设原value是百分制）
      const rating = (point.value / 20).toFixed(1)
      // 生成随机价格（100-1000元之间）
      const price = Math.floor(Math.random() * 900) + 100
      
      return {
        name,
        price,
        rating: parseFloat(rating),
        booked: false
      }
    })

    const sortedList = list.sort((a, b) => b.rating - a.rating)

    hotels.value = sortedList.map((h: any) => ({
      name: String(h.name ?? ''),
      price: Number(h.price ?? 0),
      rating: Number(h.rating ?? 0),
      booked: false,
    }))
  } catch (e) {
    showPopup('Search failed. Please try again.')
    hotels.value = []
  } finally {
    loading.value = false
  }
}
function book(hotel: HotelItem) {
  hotel.booked = true
  showPopup('预定成功')
}
function showPopup(msg: string) {
  popupMessage.value = msg
  setTimeout(() => { popupMessage.value = '' }, 2600)
}
// Fetch when query changes
watch(() => props.query, (q) => { fetchHotels(q) }, { immediate: true })
</script>
<style scoped>
.results {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.table-wrap {
  width: 60vw;
  max-width: 800px;
  margin: 28px auto 0 auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px 0 #f0f4fa;
  overflow-x: auto;
  padding: 10px 0;
}
.hotel-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: transparent;
  font-size: 1.08rem;
}
.hotel-table th {
  padding: 18px 10px 12px 10px;
  background: #f3f5fa;
  color: #2343a2;
  font-weight: bold;
  border-bottom: 2px solid #e4e9f1;
  text-align: left;
}
.hotel-table th.right {
  text-align: right;
}
.hotel-table th.center {
  text-align: center;
}
.hotel-table td {
  padding: 17px 10px 15px 10px;
  background: #fff;
  transition: background 0.18s;
  border-bottom: 1px solid #eef2f7;
  vertical-align: middle;
}
.hotel-table tr:last-child td {
  border-bottom: none;
}
.zebra td {
  background: #f9fbfd;
}
.hotel-name {
  font-size: 1.18rem;
  font-weight: 700;
  color: #1947be;
  letter-spacing: 0.3px;
  text-shadow: 0 2px 13px #eef3fe9e;
}
.rating-star {
  color: #ffe382;
  margin-right: 6px;
  font-size: 1.1em;
}
.right { text-align: right; }
.center { text-align: center; }
.book-btn {
  font-size: 1.04rem;
  font-weight: 600;
  padding: 10px 22px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(90deg, #21c97a 0%, #33b6ff 100%);
  color: #fff;
  box-shadow: 0 2px 7px #d6f2ff99;
  cursor: pointer;
  transition: background 0.18s, box-shadow 0.18s, transform 0.18s;
  outline: none;
  letter-spacing: 0.1px;
}
.book-btn:hover:not(:disabled) {
  background: linear-gradient(90deg, #389f7a 0%, #045cb1 100%);
  transform: translateY(-2px) scale(1.04);
  box-shadow: 0 4px 14px #b8e6ffe0;
}
.book-btn.booked {
  background: #c9ccd9;
  color: #6d7685;
  cursor: default;
  box-shadow: none;
}
.empty-hint, .hint {
  color: #a8b5c9;
  text-align: center;
  margin: 80px 0 30px 0;
  font-size: 1.09rem;
}
/* Toast: prominent, animated, center of page */
.reservation-toast {
  position: fixed;
  left: 50%;
  top: 16vh;
  transform: translate(-50%, 0);
  background: linear-gradient(100deg, #36e2a7 20%, #6fc5ff 100%);
  color: #ffffff;
  font-size: 1.4rem;
  padding: 18px 48px;
  box-shadow: 0 6px 38px 2px #13dbb380;
  border-radius: 16px;
  font-weight: bold;
  z-index: 2000;
  text-shadow: 0 4px 23px #20eefa7e;
  animation: jumpScale 0.45s cubic-bezier(.32,1.56,.49,.98);
}
@keyframes jumpScale {
  0% { opacity: 0; transform: translate(-50%, 20px) scale(0.7); }
  60% { opacity: 1; transform: translate(-50%, -10px) scale(1.09);}
  100% { opacity: 1; transform: translate(-50%, 0) scale(1.0); }
}
.success-fade-enter-active, .success-fade-leave-active {
  transition: opacity 0.3s;
}
.success-fade-enter-from, .success-fade-leave-to {
  opacity: 0;
}
@media (max-width: 900px) {
  .table-wrap { width: 95vw; max-width: 100vw; }
}
</style>