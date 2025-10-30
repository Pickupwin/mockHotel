<template>
  <div class="about-wrap">
    <div class="about-img-wrap">
      <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80" alt="Hotel Atmosphere" />
    </div>
    <div class="about-text">
      <h2>About Us</h2>
      <p>
        We are committed to providing a high-quality experience for every traveler.<br><br>
        Our demo site showcases modern UI, seamless hotel search, and beautiful room previews.<br><br>
        Discover, book, and enjoy a new level of hotel browsing.
      </p>
    </div>
  </div>
</template>
<script setup lang="ts">
</script>
<style scoped>
.about-wrap {
  max-width: 1100px;
  margin: 54px auto 0 auto;
  min-height: 67vh;
  background: #fff;
  display: flex;
  border-radius: 18px;
  box-shadow: 0 7px 28px #e9eefa;
  overflow: hidden;
}
.about-img-wrap {
  flex: 1 0 38%; min-width: 260px; max-width: 400px; display: flex; align-items: center; justify-content: center; background: #f0f4fa;
}
.about-img-wrap img {
  width: 100%; height: auto; display: block; object-fit: cover; border-radius: 18px 0 0 18px;
}
.about-text {
  flex: 2 1 0%; padding: 45px 38px 38px 38px; display: flex; flex-direction: column; justify-content: center; color: #304466;
}
.about-text h2 { font-size: 2.1rem; font-weight: bold; color: #2343a2; margin-bottom: 16px;}
.about-text p {
  font-size: 1.25rem;
  line-height: 1.7;
  letter-spacing: 0.01em;
}
@media (max-width: 870px) {
  .about-wrap {
    flex-direction: column;
    box-shadow: 0 5px 18px #e4eafd;
  }
  .about-img-wrap img { border-radius: 18px 18px 0 0; }
}
</style>
