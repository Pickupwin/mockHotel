import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/hotel-search': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/hotel-reserve': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/ft': {
        target: 'http://8.130.87.93:8328',
        changeOrigin: true,
      },
    },
  },
})
