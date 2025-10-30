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
              <th>Hotel</th>
              <th class="right">Price ($/night)</th>
              <th class="center">Rating</th>
              <th class="center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="hotel in hotels" :key="hotel.name" :class="{ 'zebra': $index % 2 === 1 }">
              <td>
                <span class="hotel-name">{{ hotel.name }}</span>
              </td>
              <td class="right">${{ hotel.price.toFixed(2) }}</td>
              <td class="center"><span class="rating-star">★</span>{{ hotel.rating.toFixed(1) }}</td>
              <td class="center">
                <button
                  class="book-btn"
                  @click="book(hotel)"
                  :disabled="hotel.booked"
                  :class="hotel.booked ? 'booked' : ''"
                >
                  {{ hotel.booked ? 'Booked' : 'Book' }}
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
    const list = [
      { name: "Sunrise Hotel", price: 129.0, rating: 4.5 },
      { name: "City Center Inn", price: 89.0, rating: 4.1 },
      { name: "Lakeside Resort", price: 159.0, rating: 4.7 },
    ];
    hotels.value = list.map((h: any) => ({
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
  showPopup('Booking successful!')
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