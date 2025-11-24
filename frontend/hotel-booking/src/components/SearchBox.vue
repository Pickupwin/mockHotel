<template>
  <div class="search-container">
    <form class="search-form" @submit.prevent="onSubmit">
      <input type="text" v-model="search" :placeholder="placeholder" />
      <button type="submit">Search</button>
    </form>
    <div class="toggle-container" v-if="showToggle">
      <span class="toggle-label">启动模式:</span>
      <label class="toggle-switch">
        <input type="checkbox" v-model="isFastStart" @change="onModeChange">
        <span class="slider"></span>
      </label>
      <span class="mode-label" :class="isFastStart ? 'fast' : 'normal'">
        {{ isFastStart ? '快速启动' : '普通启动' }}
      </span>
    </div>
  </div>
</template>
<script setup lang="ts">
import { defineEmits, ref, watch } from 'vue'
const emit = defineEmits(['search', 'mode-change'])
const props = defineProps<{ placeholder?: string, initial?: string, defaultMode?: 'fast' | 'normal', showToggle?: boolean }>()
const search = ref(props.initial || '')
const isFastStart = ref(props.defaultMode === 'fast' || true) // 默认为快速启动

// 当模式改变时发出事件
function onModeChange() {
  emit('mode-change', isFastStart.value ? 'fast_start' : '')
}

// 提交搜索时，同时传递搜索词和启动模式
function onSubmit() {
  emit('search', { value: search.value.trim(), provider: isFastStart.value ? 'fast_start' : '' })
}

</script>
<style scoped>
.search-container {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

.search-form {
  width: 100%;
  max-width: 500px;
  display: flex;
  gap: 9px;
  margin: 0 auto 10px auto;
}

.search-form input {
  flex: 1;
  font-size: 1.08rem;
  padding: 13px 18px;
  border: 1px solid #dde2ea;
  border-radius: 12px;
  background: #fff;
  transition: border-color 0.18s;
}

.search-form input:focus {
  border-color: #337eff;
}

.search-form button {
  background: #337eff;
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  padding: 13px 22px;
  cursor: pointer;
  font-size: 1.05rem;
}

.search-form button:hover { background: #1a4ddb; }

.toggle-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}

.toggle-label {
  font-size: 0.9rem;
  color: #4b5563;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ef4444;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #10b981;
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.mode-label {
  font-size: 0.85rem;
  font-weight: 500;
}

.mode-label.fast {
  color: #10b981;
}

.mode-label.normal {
  color: #ef4444;
}
</style>
