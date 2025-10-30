<template>
  <div class="room-preview-row">
    <div v-for="room in rooms" :key="room.title" class="room-box">
      <img :src="room.img" :alt="room.title" />
      <div class="room-title">{{ room.title }}</div>
    </div>
  </div>
</template>
<script setup lang="ts">
const rooms = [
  {
    title: 'Deluxe Room',
    img: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
  },
  {
    title: 'Suite',
    img: 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80',
  },
  {
    title: 'Family Room',
    img: 'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=400&q=80',
  },
  {
    title: 'Ocean View',
    img: 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=400&q=80',
  },
  {
    title: 'Budget Room',
    img: 'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80',
  },
]
</script>
<style scoped>
.room-preview-row {
  display: flex;
  gap: 26px;
  overflow-x: auto;
  padding: 16px 6px 6px 6px;
  margin: 0 auto 30px auto;
}
.room-box {
  min-width: 180px;
  max-width: 180px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 3px 14px 0 #f0f4fa;
  text-align: center;
  overflow: hidden;
  transition: transform 0.16s, box-shadow 0.18s;
}
.room-box:hover {
  transform: translateY(-6px) scale(1.04);
  box-shadow: 0 8px 25px 1px #e5edfa;
}
.room-box img {
  width: 100%;
  height: 110px;
  object-fit: cover;
  display: block;
}
.room-title {
  padding: 13px 0 13px 0;
  color: #253049;
  font-weight: 500;
  font-size: 1.08rem;
}
</style>
