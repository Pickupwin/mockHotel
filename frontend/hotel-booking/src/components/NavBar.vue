<template>
  <nav class="nav-bar">
    <div class="nav-left">
      <span class="site-title">HotelDemo</span>
    </div>
    <div class="nav-right">
      <router-link to="/" exact-active-class="active" class="nav-link">Home</router-link>
      <router-link to="/hotels" exact-active-class="active" class="nav-link">Hotels</router-link>
      <router-link to="/about" exact-active-class="active" class="nav-link">About</router-link>
    </div>
  </nav>
</template>
<script setup lang="ts">
</script>
<style scoped>
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: #fff;
  box-shadow: 0 3px 12px 0 #eef2f7;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}
.site-title {
  color: #2a3655;
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 2px;
}
.nav-right {
  display: flex;
  gap: 26px;
}
.nav-link {
  color: #42587a;
  text-decoration: none;
  font-size: 1.08rem;
  padding: 2px 10px;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
}
.nav-link:hover {
  background: #f5f8ff;
  color: #1a4ddb;
}
.active {
  background: #1a4ddb;
  color: #fff !important;
  font-weight: 600;
}
@media (max-width: 600px) {
  .nav-bar { padding: 0 16px; }
  .site-title { font-size: 1.1rem; }
  .nav-link { font-size: 0.95rem; }
}
</style>
