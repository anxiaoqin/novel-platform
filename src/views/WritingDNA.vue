<template>
  <div class="writing-dna-page">
    <!-- 顶部操作栏 -->
    <div class="header">
      <div class="header-left">
        <el-select 
          v-model="currentNovelId" 
          placeholder="选择作品" 
          class="novel-select"
          @change="handleNovelChange"
        >
          <el-option
            v-for="novel in novels"
            :key="novel.id"
            :label="novel.title"
            :value="novel.id"
          />
        </el-select>
      </div>
      <el-button 
        type="primary" 
        @click="startAnalyze"
        :disabled="!currentNovelId || analyzing"
        :loading="analyzing"
      >
        <el-icon v-if="!analyzing"><MagicStick /></el-icon>
        {{ analyzing ? '分析中...' : '分析写作风格' }}
      </el-button>
    </div>

    <!-- 分析进度 -->
    <div class="analyze-progress" v-if="analyzing">
      <el-card>
        <div class="progress-content">
          <el-progress
            :percentage="progressPercent"
            :status="progressStatus"
            :stroke-width="12"
          />
          <p class="progress-tip">{{ progressTip }}</p>
        </div>
      </el-card>
    </div>

    <!-- DNA分析结果 -->
    <div class="dna-results" v-if="dnaProfile && !analyzing">
      <!-- DNA画像卡片 -->
      <div class="dna-header">
        <el-card class="fingerprint-card">
          <template #header>
            <div class="card-header">
              <span class="title">🧬 写作DNA画像</span>
            </div>
          </template>
          <div class="fingerprint-content">
            <div class="fingerprint-name">{{ dnaProfile.style_fingerprint || '待分析' }}</div>
            <p class="fingerprint-desc">
              基于{{ chapterCount }}章内容的综合分析
            </p>
          </div>
        </el-card>
      </div>

      <!-- 五维雷达图 -->
      <div class="radar-section">
        <el-card>
          <template #header>
            <span class="section-title">📊 五维能力图谱</span>
          </template>
          <div class="radar-container">
            <div class="radar-chart" ref="radarChartRef"></div>
            <div class="radar-legend">
              <div class="legend-item">
                <span class="legend-color" style="background: #667eea"></span>
                <span class="legend-label">句式特征</span>
                <span class="legend-value">{{ dnaProfile.sentence_patterns?.rhythm || '未知' }}</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #f093fb"></span>
                <span class="legend-label">词汇偏好</span>
                <span class="legend-value">{{ dnaProfile.vocabulary?.formal_level || '未知' }}</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #4facfe"></span>
                <span class="legend-label">叙事风格</span>
                <span class="legend-value">{{ dnaProfile.narrative_style?.perspective || '未知' }}</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #43e97b"></span>
                <span class="legend-label">情感基调</span>
                <span class="legend-value">{{ dnaProfile.emotion_tone?.overall_tone || '未知' }}</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #fa709a"></span>
                <span class="legend-label">幽默指数</span>
                <span class="legend-value">{{ dnaProfile.emotion_tone?.humor_level || '低' }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 详细数据 -->
      <div class="detail-section">
        <el-row :gutter="20">
          <!-- 独特特征 -->
          <el-col :span="12">
            <el-card>
              <template #header>
                <span class="section-title">✨ 独特写作特征</span>
              </template>
              <div class="traits-list">
                <div 
                  v-for="(trait, idx) in dnaProfile.unique_traits" 
                  :key="idx"
                  class="trait-item"
                >
                  <el-icon><Check /></el-icon>
                  <span>{{ trait }}</span>
                </div>
                <el-empty v-if="!dnaProfile.unique_traits?.length" description="暂无特征" />
              </div>
            </el-card>
          </el-col>
          
          <!-- 常用词汇 -->
          <el-col :span="12">
            <el-card>
              <template #header>
                <span class="section-title">📝 高频使用词汇</span>
              </template>
              <div class="fav-words">
                <el-tag
                  v-for="word in dnaProfile.vocabulary?.fav_words"
                  :key="word"
                  size="large"
                  class="word-tag"
                >
                  {{ word }}
                </el-tag>
                <el-empty v-if="!dnaProfile.vocabulary?.fav_words?.length" description="暂无数据" />
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 句式分析 -->
      <div class="sentence-section">
        <el-card>
          <template #header>
            <span class="section-title">📏 句式特征</span>
          </template>
          <div class="sentence-stats">
            <div class="stat-item">
              <span class="stat-label">平均句长</span>
              <span class="stat-value">{{ dnaProfile.sentence_patterns?.avg_length || '未知' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">节奏特点</span>
              <span class="stat-value">{{ dnaProfile.sentence_patterns?.rhythm || '未知' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">对话占比</span>
              <span class="stat-value">{{ dnaProfile.narrative_style?.dialogue_ratio || '中等' }}</span>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 历史记录 -->
      <div class="history-section" v-if="dnaHistory.length > 1">
        <el-card>
          <template #header>
            <span class="section-title">📜 历史DNA记录</span>
          </template>
          <div class="history-list">
            <div 
              v-for="(record, idx) in dnaHistory"
              :key="idx"
              class="history-item"
              :class="{ active: idx === 0 }"
            >
              <div class="history-info">
                <span class="history-time">{{ formatDate(record.created_at) }}</span>
                <span class="history-fingerprint">{{ record.style_fingerprint || '风格分析' }}</span>
              </div>
              <el-tag v-if="idx === 0" size="small" type="primary">最新</el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-if="!dnaProfile && !analyzing && currentNovelId">
      <el-empty description="暂无写作DNA数据">
        <el-button type="primary" @click="startAnalyze">开始分析</el-button>
      </el-empty>
    </div>

    <el-empty v-if="!currentNovelId" description="请先选择作品" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { MagicStick, Check } from '@element-plus/icons-vue'
import { analyzeWritingDNA, getWritingDNA } from '@/api/modules/ai'
import { getNovels } from '@/api/modules/novel'
import { getChapters } from '@/api/modules/chapter'

// 状态
const novels = ref([])
const currentNovelId = ref(null)
const analyzing = ref(false)
const progressPercent = ref(0)
const progressTip = ref('正在准备分析...')
const progressStatus = ref('')
const dnaProfile = ref(null)
const dnaHistory = ref([])
const chapterCount = ref(0)
const radarChartRef = ref(null)
let chartInstance = null

// 获取作品列表
const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.data || []
    if (novels.value.length && !currentNovelId.value) {
      currentNovelId.value = novels.value[0].id
      loadWritingDNA()
    }
  } catch (err) {
    console.error('加载作品列表失败:', err)
  }
}

// 加载写作DNA
const loadWritingDNA = async () => {
  if (!currentNovelId.value) return
  try {
    const res = await getWritingDNA(currentNovelId.value)
    if (res.data) {
      dnaProfile.value = res.data.profile || res.data
      dnaHistory.value = Array.isArray(res.data) ? res.data : [res.data]
      chapterCount.value = res.data.chapter_count || 0
      await nextTick()
      renderRadarChart()
    }
  } catch (err) {
    console.error('加载写作DNA失败:', err)
    // 没有数据时不报错
  }
}

// 加载章节数量
const loadChapterCount = async () => {
  if (!currentNovelId.value) return 0
  try {
    const res = await getChapters(currentNovelId.value)
    const chapters = res.data?.items || res.data || []
    chapterCount.value = chapters.length
    return chapters.length
  } catch (err) {
    console.error('加载章节失败:', err)
    return 0
  }
}

// 作品切换
const handleNovelChange = () => {
  dnaProfile.value = null
  loadWritingDNA()
}

// 开始分析
const startAnalyze = async () => {
  analyzing.value = true
  progressPercent.value = 0
  progressTip.value = '正在获取章节内容...'
  progressStatus.value = ''
  
  try {
    // 获取章节数量
    const count = await loadChapterCount()
    progressPercent.value = 20
    progressTip.value = `发现 ${count} 个章节，正在分析...`
    
    if (count === 0) {
      ElMessage.warning('该作品暂无章节内容，请先创作后再分析')
      analyzing.value = false
      return
    }
    
    // 模拟进度
    const progressInterval = setInterval(() => {
      if (progressPercent.value < 80) {
        progressPercent.value += 10
        const tips = [
          '正在提取句式特征...',
          '正在分析词汇偏好...',
          '正在识别叙事风格...',
          '正在解析情感基调...',
          '正在生成DNA画像...'
        ]
        progressTip.value = tips[Math.floor(progressPercent.value / 20) - 1] || '分析中...'
      }
    }, 300)
    
    // 调用分析API
    const res = await analyzeWritingDNA({ novel_id: currentNovelId.value })
    
    clearInterval(progressInterval)
    progressPercent.value = 100
    progressTip.value = '分析完成！'
    progressStatus.value = 'success'
    
    // 更新数据
    if (res.data) {
      dnaProfile.value = res.data.profile || res.data
      dnaHistory.value.unshift({
        ...dnaProfile.value,
        created_at: new Date().toISOString()
      })
    }
    
    ElMessage.success('写作风格分析完成！')
    
    // 关闭进度显示并渲染图表
    setTimeout(() => {
      analyzing.value = false
      nextTick(() => renderRadarChart())
    }, 1000)
    
  } catch (err) {
    console.error('分析失败:', err)
    progressStatus.value = 'exception'
    progressTip.value = '分析失败，请重试'
    ElMessage.error('写作风格分析失败')
    setTimeout(() => {
      analyzing.value = false
    }, 1500)
  }
}

// 渲染雷达图
const renderRadarChart = () => {
  if (!radarChartRef.value || !dnaProfile.value) return
  
  // 简单模拟的雷达图数据（实际应从后端获取）
  const profile = dnaProfile.value
  const data = [
    {
      name: '句式特征',
      value: 80,
      max: 100
    },
    {
      name: '词汇偏好',
      value: profile.vocabulary?.score || 70,
      max: 100
    },
    {
      name: '叙事风格',
      value: 75,
      max: 100
    },
    {
      name: '情感基调',
      value: profile.emotion_tone?.score || 65,
      max: 100
    },
    {
      name: '节奏把控',
      value: 70,
      max: 100
    }
  ]
  
  // 使用简单的Canvas绘制或SVG
  const container = radarChartRef.value
  container.innerHTML = ''
  
  // 创建SVG雷达图
  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS, 'svg')
  svg.setAttribute('width', '300')
  svg.setAttribute('height', '300')
  svg.setAttribute('viewBox', '0 0 300 300')
  
  const centerX = 150
  const centerY = 150
  const radius = 100
  const sides = 5
  const angleStep = (Math.PI * 2) / sides
  const startAngle = -Math.PI / 2
  
  // 绘制背景网格
  const colors = ['#f0f0f0', '#e0e0e0', '#d0d0d0', '#c0c0c0', '#b0b0b0']
  colors.forEach((color, level) => {
    const r = radius * ((level + 1) / 5)
    const points = []
    for (let i = 0; i < sides; i++) {
      const angle = startAngle + angleStep * i
      const x = centerX + r * Math.cos(angle)
      const y = centerY + r * Math.sin(angle)
      points.push(`${x},${y}`)
    }
    const polygon = document.createElementNS(svgNS, 'polygon')
    polygon.setAttribute('points', points.join(' '))
    polygon.setAttribute('fill', color)
    polygon.setAttribute('stroke', '#ddd')
    polygon.setAttribute('stroke-width', '1')
    svg.appendChild(polygon)
  })
  
  // 绘制轴线
  for (let i = 0; i < sides; i++) {
    const angle = startAngle + angleStep * i
    const x = centerX + radius * Math.cos(angle)
    const y = centerY + radius * Math.sin(angle)
    const line = document.createElementNS(svgNS, 'line')
    line.setAttribute('x1', centerX)
    line.setAttribute('y1', centerY)
    line.setAttribute('x2', x)
    line.setAttribute('y2', y)
    line.setAttribute('stroke', '#ccc')
    line.setAttribute('stroke-width', '1')
    svg.appendChild(line)
    
    // 标签
    const labelX = centerX + (radius + 25) * Math.cos(angle)
    const labelY = centerY + (radius + 25) * Math.sin(angle)
    const text = document.createElementNS(svgNS, 'text')
    text.setAttribute('x', labelX)
    text.setAttribute('y', labelY)
    text.setAttribute('text-anchor', 'middle')
    text.setAttribute('dominant-baseline', 'middle')
    text.setAttribute('font-size', '12')
    text.setAttribute('fill', '#666')
    text.textContent = data[i].name
    svg.appendChild(text)
  }
  
  // 绘制数据区域
  const dataPoints = data.map((d, i) => {
    const angle = startAngle + angleStep * i
    const r = (d.value / 100) * radius
    return {
      x: centerX + r * Math.cos(angle),
      y: centerY + r * Math.sin(angle)
    }
  })
  
  const dataPolygon = document.createElementNS(svgNS, 'polygon')
  dataPolygon.setAttribute('points', dataPoints.map(p => `${p.x},${p.y}`).join(' '))
  dataPolygon.setAttribute('fill', 'rgba(102, 126, 234, 0.3)')
  dataPolygon.setAttribute('stroke', '#667eea')
  dataPolygon.setAttribute('stroke-width', '2')
  svg.appendChild(dataPolygon)
  
  // 绘制数据点
  dataPoints.forEach((p, i) => {
    const circle = document.createElementNS(svgNS, 'circle')
    circle.setAttribute('cx', p.x)
    circle.setAttribute('cy', p.y)
    circle.setAttribute('r', '5')
    circle.setAttribute('fill', '#667eea')
    svg.appendChild(circle)
    
    // 数据值
    const valueText = document.createElementNS(svgNS, 'text')
    valueText.setAttribute('x', p.x)
    valueText.setAttribute('y', p.y - 12)
    valueText.setAttribute('text-anchor', 'middle')
    valueText.setAttribute('font-size', '11')
    valueText.setAttribute('fill', '#667eea')
    valueText.setAttribute('font-weight', 'bold')
    valueText.textContent = data[i].value
    svg.appendChild(valueText)
  })
  
  container.appendChild(svg)
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 组件卸载时清理
onUnmounted(() => {
  if (chartInstance) {
    chartInstance = null
  }
})

// 初始化
onMounted(() => {
  loadNovels()
})
</script>

<style scoped>
.writing-dna-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.novel-select {
  width: 240px;
}

/* 分析进度 */
.analyze-progress {
  margin-bottom: 24px;
}

.progress-content {
  padding: 20px;
}

.progress-content .el-progress {
  margin-bottom: 16px;
}

.progress-tip {
  text-align: center;
  color: #666;
  margin: 0;
}

/* DNA结果 */
.dna-results {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dna-header .fingerprint-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.dna-header .card-header .title {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.fingerprint-content {
  text-align: center;
  padding: 20px 0;
}

.fingerprint-name {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.fingerprint-desc {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
}

/* 雷达图 */
.radar-section .section-title {
  font-size: 16px;
  font-weight: 600;
}

.radar-container {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 20px 0;
}

.radar-chart {
  width: 300px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-label {
  font-size: 13px;
  color: #666;
  min-width: 70px;
}

.legend-value {
  font-size: 13px;
  font-weight: 500;
  color: #333;
}

/* 特征列表 */
.detail-section .section-title {
  font-size: 16px;
  font-weight: 600;
}

.traits-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.trait-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #f9f9f9;
  border-radius: 6px;
  color: #555;
}

.trait-item .el-icon {
  color: #67c23a;
}

/* 常用词汇 */
.fav-words {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.word-tag {
  padding: 8px 16px;
  font-size: 14px;
}

/* 句式分析 */
.sentence-section .section-title {
  font-size: 16px;
  font-weight: 600;
}

.sentence-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

/* 历史记录 */
.history-section .section-title {
  font-size: 16px;
  font-weight: 600;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 6px;
  background: #f9f9f9;
}

.history-item.active {
  background: #ecf5ff;
  border-left: 3px solid #409eff;
}

.history-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-time {
  font-size: 12px;
  color: #999;
}

.history-fingerprint {
  font-size: 14px;
  color: #333;
}

/* 响应式 */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .novel-select {
    width: 100%;
  }
  
  .radar-container {
    flex-direction: column;
    gap: 20px;
  }
  
  .detail-section .el-col {
    margin-bottom: 20px;
  }
}
</style>
