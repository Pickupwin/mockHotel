import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// Vue Router setup
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Home from './views/Home.vue'
import Hotels from './views/Hotels.vue'
import About from './views/About.vue'
import Technical from './views/Technical.vue'

const routes: RouteRecordRaw[] = [
  { path: '/', name: 'Home', component: Home },
  { path: '/hotels', name: 'Hotels', component: Hotels },
  { path: '/about', name: 'About', component: About },
  { path: '/technical', name: 'Technical', component: Technical },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).mount('#app')
