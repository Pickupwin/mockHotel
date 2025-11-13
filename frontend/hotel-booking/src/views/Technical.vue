<template>
  <div class="technical-page">
    <h1 class="page-title">技术效果对比</h1>
    <div class="content-container">
      <div class="control-panel">
        <h3>启动选项</h3>
        <button 
          class="control-btn quick-start"
          @click="handleQuickStart"
          :disabled="isLoading"
        >
          {{ isLoading && loadingType === 'quick' ? '加载中...' : '快速启动' }}
        </button>
        <button 
          class="control-btn normal-start"
          @click="handleNormalStart"
          :disabled="isLoading"
        >
          {{ isLoading && loadingType === 'normal' ? '加载中...' : '普通启动' }}
        </button>
        <div class="chart-info" v-if="showLegend">
          <div class="legend-item">
            <span class="legend-color quick-color"></span>
            <span class="legend-text">快速启动</span>
          </div>
          <div class="legend-item">
            <span class="legend-color normal-color"></span>
            <span class="legend-text">普通启动</span>
          </div>
        </div>
      </div>
      <div class="chart-container">
        <canvas ref="chartCanvas" width="800" height="400"></canvas>
        <div v-if="!hasData" class="empty-state">
          <p>点击左侧按钮获取数据并查看性能对比</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

// 状态管理
const chartCanvas = ref<HTMLCanvasElement | null>(null)
const isLoading = ref(false)
const loadingType = ref<'quick' | 'normal' | null>(null)
const hasData = ref(false)
const showLegend = ref(false)

// 数据存储
const quickStartData = ref<{x: number[], y: number[]} | null>(null)
const normalStartData = ref<{x: number[], y: number[]} | null>(null)

// 处理快速启动
async function handleQuickStart() {
  isLoading.value = true
  loadingType.value = 'quick'
  try {
    const response = await axios.get('/hotel-search/quick-start')
    quickStartData.value = response.data
    hasData.value = true
    showLegend.value = true
    await nextTick()
    drawChart()
  } catch (error) {
    console.error('获取快速启动数据失败:', error)
  } finally {
    isLoading.value = false
    loadingType.value = null
  }
}

// 处理普通启动
async function handleNormalStart() {
  isLoading.value = true
  loadingType.value = 'normal'
  try {
    const response = await axios.get('/hotel-search/normal-start')
    normalStartData.value = response.data
    hasData.value = true
    showLegend.value = true
    await nextTick()
    drawChart()
  } catch (error) {
    console.error('获取普通启动数据失败:', error)
  } finally {
    isLoading.value = false
    loadingType.value = null
  }
}

// 绘制图表
function drawChart() {
  if (!chartCanvas.value) return
  
  const ctx = chartCanvas.value.getContext('2d')
  if (!ctx) return
  
  // 清除画布
  ctx.clearRect(0, 0, chartCanvas.value.width, chartCanvas.value.height)
  
  const margin = { top: 20, right: 220, bottom: 40, left: 60 }
  const width = chartCanvas.value.width - margin.left - margin.right
  const height = chartCanvas.value.height - margin.top - margin.bottom
  
  // 设置样式
  ctx.strokeStyle = '#1a4ddb'
  ctx.fillStyle = '#1a4ddb'
  ctx.font = '12px Inter, Helvetica, sans-serif'
  
  // 计算全局最大值用于所有数据的归一化
  let globalMaxX = 0
  let globalMaxY = 0
  
  if (quickStartData.value) {
    globalMaxX = Math.max(globalMaxX, Math.max(...quickStartData.value.x))
    globalMaxY = Math.max(globalMaxY, Math.max(...quickStartData.value.y))
  }
  
  if (normalStartData.value) {
    globalMaxX = Math.max(globalMaxX, Math.max(...normalStartData.value.x))
    globalMaxY = Math.max(globalMaxY, Math.max(...normalStartData.value.y))
  }
  
  // 绘制坐标轴
  drawAxes(ctx, margin, width, height, globalMaxX, globalMaxY)
  
  // 绘制数据
  if (quickStartData.value) {
    ctx.strokeStyle = '#10b981' // 绿色表示快速启动
    ctx.lineWidth = 2
    drawLine(ctx, quickStartData.value, margin, width, height, globalMaxX, globalMaxY)
  }
  
  if (normalStartData.value) {
    ctx.strokeStyle = '#ef4444' // 红色表示普通启动
    ctx.lineWidth = 2
    drawLine(ctx, normalStartData.value, margin, width, height, globalMaxX, globalMaxY)
  }
}

// 绘制坐标轴
function drawAxes(ctx: CanvasRenderingContext2D, margin: any, width: number, height: number, maxX: number, maxY: number) {
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 1
  
  // X轴
  ctx.beginPath()
  ctx.moveTo(margin.left, margin.top + height)
  ctx.lineTo(margin.left + width, margin.top + height)
  ctx.stroke()
  
  // Y轴
  ctx.beginPath()
  ctx.moveTo(margin.left, margin.top)
  ctx.lineTo(margin.left, margin.top + height)
  ctx.stroke()
  
  // X轴标签
  ctx.fillStyle = '#4b5563'
  ctx.fillText('时间(ms)', margin.left + width / 2 - 20, margin.top + height + 30)
  
  // Y轴标签（旋转）
  ctx.save()
  ctx.translate(margin.left - 40, margin.top + height / 2)
  ctx.rotate(-Math.PI / 2)
  ctx.fillText('实例数目', -30, 0)
  ctx.restore()
  
  // 网格线
  ctx.strokeStyle = '#f3f4f6'
  ctx.lineWidth = 1
  
  // 水平网格线和Y轴刻度
  for (let i = 0; i <= 5; i++) {
    const y = margin.top + (height / 5) * i
    ctx.beginPath()
    ctx.moveTo(margin.left, y)
    ctx.lineTo(margin.left + width, y)
    ctx.stroke()
    
    // Y轴刻度标签 - 使用真实的最大值
    const value = Math.round((maxY / 5) * (5 - i))
    ctx.fillStyle = '#6b7280'
    ctx.fillText(value.toString(), margin.left - 30, y + 4)
  }
  
  // 垂直网格线和X轴刻度
  for (let i = 0; i <= 5; i++) {
    const x = margin.left + (width / 5) * i
    ctx.beginPath()
    ctx.moveTo(x, margin.top)
    ctx.lineTo(x, margin.top + height)
    ctx.stroke()
    
    // X轴刻度标签 - 使用真实的最大值
    const value = Math.round((maxX / 5) * i)
    ctx.fillStyle = '#6b7280'
    ctx.fillText(value.toString(), x - 15, margin.top + height + 15)
  }
}

// 绘制数据曲线
function drawLine(ctx: CanvasRenderingContext2D, data: {x: number[], y: number[]}, margin: any, width: number, height: number, globalMaxX: number, globalMaxY: number) {
  if (!data.x.length || !data.y.length || globalMaxX === 0 || globalMaxY === 0) return
  
  ctx.beginPath()
  
  data.x.forEach((x, index) => {
    // 使用全局最大值进行归一化，确保两种方法在相同坐标系统下比较
    const normalizedX = margin.left + (x / globalMaxX) * width
    const normalizedY = margin.top + height - (data.y[index] / globalMaxY) * height
    
    if (index === 0) {
      ctx.moveTo(normalizedX, normalizedY)
    } else {
      ctx.lineTo(normalizedX, normalizedY)
    }
  })
  
  ctx.stroke()
}

// 窗口大小变化时重新绘制
onMounted(() => {
  window.addEventListener('resize', drawChart)
  return () => window.removeEventListener('resize', drawChart)
})
</script>

<style scoped>
.technical-page {
  max-width: 1200px;
  margin: 38px auto 0 auto;
  padding: 0 20px;
  min-height: 70vh;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  color: #23377b;
  margin-bottom: 32px;
}

.content-container {
  display: flex;
  gap: 32px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 24px;
}

.control-panel {
  flex: 0 0 280px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.control-panel h3 {
  margin: 0 0 8px 0;
  color: #2d3748;
  font-size: 1.1rem;
  font-weight: 600;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.control-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.control-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.quick-start {
  background-color: #10b981;
  color: white;
}

.quick-start:hover:not(:disabled) {
  background-color: #059669;
}

.normal-start {
  background-color: #ef4444;
  color: white;
}

.normal-start:hover:not(:disabled) {
  background-color: #dc2626;
}

.chart-container {
  flex: 1;
  position: relative;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background-color: #fafafa;
  overflow: hidden;
}

.chart-info {
  margin-top: 24px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: #4b5563;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.quick-color {
  background-color: #10b981;
}

.normal-color {
  background-color: #ef4444;
}

.empty-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #9ca3af;
  font-size: 1.1rem;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }
  
  .control-panel {
    flex: none;
  }
  
  .chart-container {
    min-height: 300px;
  }
}
</style>