<template>
  <div class="step-analysis-container">
    <!-- 顶部导航 -->
    <header class="analysis-header">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <h2 class="page-title">AI段落分析</h2>
      </div>
      <div class="header-right">
        <el-button size="small" @click="loadHistory">
          <el-icon><Clock /></el-icon> 历史记录
        </el-button>
      </div>
    </header>

    <!-- 主体内容 -->
    <div class="analysis-main">
      <!-- 左侧输入区 -->
      <main class="input-area">
        <div class="input-header">
          <span class="section-label">待分析段落</span>
          <div class="input-actions">
            <el-button size="small" @click="pasteFromClipboard">
              <el-icon><DocumentCopy /></el-icon> 粘贴
            </el-button>
            <el-button size="small" @click="clearInput">
              <el-icon><Delete /></el-icon> 清空
            </el-button>
          </div>
        </div>
        
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="10"
          placeholder="输入或粘贴需要分析的段落内容..."
          @input="handleInputChange"
        />
        
        <!-- 快捷操作 -->
        <div class="quick-actions">
          <el-button type="primary" :loading="analysisLoading" @click="startAnalysis">
            <el-icon><MagicStick /></el-icon> 开始分析
          </el-button>
          <el-button :disabled="!inputText" @click="startStreamAnalysis">
            <el-icon><VideoPlay /></el-icon> 流式分析
          </el-button>
        </div>

        <!-- 实时输出区 -->
        <div class="realtime-output" v-if="isStreaming || streamContent">
          <div class="output-header">
            <span class="section-label">实时分析结果</span>
            <el-tag v-if="isStreaming" type="success" size="small" effect="dark">
              <span class="pulse-dot"></span> AI分析中
            </el-tag>
          </div>
          <div class="output-content" v-html="renderedStreamContent"></div>
          <div class="streaming-cursor" v-if="isStreaming">|</div>
        </div>

        <!-- 配置选项 -->
        <div class="config-section" v-if="!isStreaming && !streamContent">
          <div class="section-title">分析配置</div>
          
          <div class="config-item">
            <span class="config-label">上下文模式</span>
            <el-radio-group v-model="config.contextMode" size="small">
              <el-radio-button label="auto">自动</el-radio-button>
              <el-radio-button label="manual">手动</el-radio-button>
            </el-radio-group>
          </div>
          
          <div class="config-item">
            <span class="config-label">分析粒度</span>
            <el-radio-group v-model="config.granularity" size="small">
              <el-radio-button label="chapter">章节</el-radio-button>
              <el-radio-button label="scene">场景</el-radio-button>
              <el-radio-button label="paragraph">段落</el-radio-button>
            </el-radio-group>
          </div>
          
          <div class="config-item">
            <span class="config-label">最大建议数</span>
            <el-slider v-model="config.maxSuggestions" :min="3" :max="8" :step="1" show-input size="small" />
          </div>
        </div>
      </main>

      <!-- 右侧结果区 -->
      <aside class="result-area" v-if="analysisResult">
        <!-- 提取元素 -->
        <div class="result-section extracted-elements">
          <div class="section-header">
            <span class="section-label">提取的元素</span>
          </div>
          
          <div class="element-grid">
            <!-- 角色 -->
            <div class="element-card" v-if="analysisResult.extracted?.characters?.length">
              <div class="card-icon">👤</div>
              <div class="card-title">角色</div>
              <div class="card-items">
                <el-tag
                  v-for="char in analysisResult.extracted.characters"
                  :key="char.name"
                  size="small"
                  :type="char.role === '主角' ? 'primary' : 'info'"
                >
                  {{ char.name }} ({{ char.role }})
                </el-tag>
              </div>
            </div>
            
            <!-- 地点 -->
            <div class="element-card" v-if="analysisResult.extracted?.locations?.length">
              <div class="card-icon">📍</div>
              <div class="card-title">地点</div>
              <div class="card-items">
                <el-tag v-for="loc in analysisResult.extracted.locations" :key="loc" size="small">
                  {{ loc }}
                </el-tag>
              </div>
            </div>
            
            <!-- 冲突 -->
            <div class="element-card" v-if="analysisResult.extracted?.conflicts?.length">
              <div class="card-icon">⚔️</div>
              <div class="card-title">冲突</div>
              <div class="card-items">
                <el-tag v-for="conflict in analysisResult.extracted.conflicts" :key="conflict" size="small" type="warning">
                  {{ conflict }}
                </el-tag>
              </div>
            </div>
            
            <!-- 情感 -->
            <div class="element-card" v-if="analysisResult.extracted?.emotions?.length">
              <div class="card-icon">💭</div>
              <div class="card-title">情感</div>
              <div class="card-items">
                <el-tag v-for="emotion in analysisResult.extracted.emotions" :key="emotion" size="small" type="danger">
                  {{ emotion }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- 事件建议 -->
        <div class="result-section event-suggestions">
          <div class="section-header">
            <span class="section-label">事件建议</span>
            <el-select v-model="filterType" size="small" placeholder="筛选类型" clearable>
              <el-option label="全部" value="" />
              <el-option label="铺垫" value="铺垫" />
              <el-option label="冲突" value="冲突" />
              <el-option label="反转" value="反转" />
              <el-option label="高潮" value="高潮" />
              <el-option label="过渡" value="过渡" />
              <el-option label="收尾" value="收尾" />
            </el-select>
          </div>
          
          <div class="suggestions-list">
            <div
              v-for="suggestion in filteredSuggestions"
              :key="suggestion.id"
              class="suggestion-item"
              :class="{ expanded: expandedSuggestions.includes(suggestion.id) }"
            >
              <div class="item-header" @click="toggleSuggestion(suggestion.id)">
                <el-tag size="small" :type="getTypeColor(suggestion.type)">
                  {{ suggestion.type }}
                </el-tag>
                <span class="item-title">{{ suggestion.title }}</span>
                <el-icon class="expand-icon">
                  <ArrowRight v-if="!expandedSuggestions.includes(suggestion.id)" />
                  <ArrowDown v-else />
                </el-icon>
              </div>
              
              <div class="item-body" v-show="expandedSuggestions.includes(suggestion.id)">
                <div class="item-description">
                  <span class="label">描述：</span>
                  {{ suggestion.description }}
                </div>
                
                <div class="item-participants" v-if="suggestion.participants?.length">
                  <span class="label">参与者：</span>
                  <el-tag
                    v-for="p in suggestion.participants"
                    :key="p"
                    size="small"
                  >
                    {{ p }}
                  </el-tag>
                </div>
                
                <div class="item-reasoning">
                  <span class="label">推理：</span>
                  {{ suggestion.reasoning }}
                </div>
                
                <div class="item-followups" v-if="suggestion.follow_ups?.length">
                  <span class="label">后续发展：</span>
                  <ul>
                    <li v-for="(f, idx) in suggestion.follow_ups" :key="idx">{{ f }}</li>
                  </ul>
                </div>
                
                <div class="item-actions">
                  <el-button size="small" type="primary" @click="applySuggestion(suggestion)">
                    应用到大纲
                  </el-button>
                  <el-button size="small" @click="previewSuggestion(suggestion)">
                    预览展开
                  </el-button>
                </div>
              </div>
            </div>
            
            <el-empty v-if="!filteredSuggestions.length" description="暂无建议" />
          </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="result-actions" v-if="analysisResult">
          <el-button type="primary" @click="applyAllSuggestions">
            <el-icon><Check /></el-icon> 应用全部建议
          </el-button>
          <el-button @click="exportAnalysis">
            <el-icon><Download /></el-icon> 导出分析报告
          </el-button>
        </div>
      </aside>
    </div>

    <!-- 预览对话框 -->
    <el-dialog v-model="previewDialogVisible" title="事件展开预览" width="600px">
      <div class="preview-content" v-if="previewData">
        <h3>{{ previewData.title }}</h3>
        <p class="preview-type">
          <el-tag :type="getTypeColor(previewData.type)">{{ previewData.type }}</el-tag>
        </p>
        <div class="preview-section">
          <strong>事件描述：</strong>
          <p>{{ previewData.description }}</p>
        </div>
        <div class="preview-section" v-if="previewData.participants?.length">
          <strong>参与者：</strong>
          <div class="preview-tags">
            <el-tag v-for="p in previewData.participants" :key="p">{{ p }}</el-tag>
          </div>
        </div>
        <div class="preview-section">
          <strong>推理逻辑：</strong>
          <p>{{ previewData.reasoning }}</p>
        </div>
        <div class="preview-section" v-if="previewData.follow_ups?.length">
          <strong>后续发展：</strong>
          <ul>
            <li v-for="(f, idx) in previewData.follow_ups" :key="idx">{{ f }}</li>
          </ul>
        </div>
      </div>
      <template #footer>
        <el-button @click="previewDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="applyPreviewSuggestion">应用到大纲</el-button>
      </template>
    </el-dialog>

    <!-- 历史记录对话框 -->
    <el-dialog v-model="historyDialogVisible" title="分析历史" width="700px">
      <div class="history-list">
        <div
          v-for="item in historyList"
          :key="item.id"
          class="history-item"
          @click="loadHistoryItem(item)"
        >
          <div class="history-header">
            <span class="history-time">{{ formatTime(item.created_at) }}</span>
            <el-tag size="small" type="info">{{ item.granularity }}</el-tag>
          </div>
          <div class="history-preview">{{ item.content?.substring(0, 100) }}...</div>
          <div class="history-stats">
            提取了 {{ item.extracted_count || 0 }} 个元素，生成 {{ item.suggestion_count || 0 }} 条建议
          </div>
        </div>
        <el-empty v-if="!historyList.length" description="暂无历史记录" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft, MagicStick, VideoPlay, Clock, DocumentCopy,
  Delete, ArrowRight, ArrowDown, Check, Download
} from '@element-plus/icons-vue'
import { createSSEStream, extractContent } from '@/api/sse'
import api from '@/api'

// 路由
const router = useRouter()
const route = useRoute()

// 状态
const novelId = ref(route.query.novel_id || 1)
const chapterId = ref(route.query.chapter_id || 1)
const inputText = ref('')
const analysisResult = ref(null)
const analysisLoading = ref(false)

// 流式分析状态
const isStreaming = ref(false)
const streamContent = ref('')
const streamController = ref(null)

// 配置
const config = reactive({
  contextMode: 'auto',
  granularity: 'scene',
  maxSuggestions: 5
})

// 筛选
const filterType = ref('')
const expandedSuggestions = ref([])

// 预览
const previewDialogVisible = ref(false)
const previewData = ref(null)

// 历史记录
const historyDialogVisible = ref(false)
const historyList = ref([])

// 计算属性
const filteredSuggestions = computed(() => {
  if (!analysisResult.value?.suggestions) return []
  if (!filterType.value) return analysisResult.value.suggestions
  return analysisResult.value.suggestions.filter(s => s.type === filterType.value)
})

const renderedStreamContent = computed(() => {
  // 简单的markdown渲染
  return streamContent.value
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/^### (.*$)/gm, '<h4>$1</h4>')
    .replace(/^## (.*$)/gm, '<h3>$1</h3>')
    .replace(/^# (.*$)/gm, '<h2>$1</h2>')
    .replace(/\n/g, '<br>')
})

// 生命周期
onMounted(() => {
  // 从URL参数加载文本
  if (route.query.content) {
    inputText.value = decodeURIComponent(route.query.content)
  }
})

onUnmounted(() => {
  if (streamController.value) {
    streamController.value.abort()
  }
})

// 方法
function goBack() {
  router.back()
}

function handleInputChange() {
  // 清除之前的分析结果
  analysisResult.value = null
  streamContent.value = ''
}

async function pasteFromClipboard() {
  try {
    const text = await navigator.clipboard.readText()
    inputText.value = text
    handleInputChange()
    ElMessage.success('已粘贴')
  } catch (err) {
    ElMessage.error('粘贴失败，请手动粘贴')
  }
}

function clearInput() {
  ElMessageBox.confirm('确定清空输入内容？').then(() => {
    inputText.value = ''
    analysisResult.value = null
    streamContent.value = ''
  }).catch(() => {})
}

// 开始非流式分析
async function startAnalysis() {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入需要分析的段落')
    return
  }
  
  analysisLoading.value = true
  analysisResult.value = null
  
  try {
    const res = await api.post('/ai/analyze-paragraph', {
      paragraph: inputText.value,
      novel_id: novelId.value,
      context_mode: config.contextMode,
      max_suggestions: config.maxSuggestions,
      granularity: config.granularity
    })
    
    if (res.data.success) {
      analysisResult.value = res.data.data
      ElMessage.success('分析完成')
    }
  } catch (err) {
    ElMessage.error('分析失败: ' + (err.message || '未知错误'))
  } finally {
    analysisLoading.value = false
  }
}

// 开始流式分析
function startStreamAnalysis() {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入需要分析的段落')
    return
  }
  
  isStreaming.value = true
  streamContent.value = ''
  analysisResult.value = null
  
  streamController.value = createSSEStream('/ai/analyze-paragraph/stream', {
    paragraph: inputText.value,
    novel_id: novelId.value,
    context_mode: config.contextMode,
    max_suggestions: config.maxSuggestions,
    granularity: config.granularity
  }, {
    onMessage: (data) => {
      // 处理增量数据
      const content = extractContent(data)
      if (content) {
        streamContent.value += content
      }
      
      // 尝试解析完整结果
      if (data.extracted || data.suggestions) {
        analysisResult.value = data
      }
    },
    onDone: () => {
      isStreaming.value = false
      // 尝试从流内容解析最终结果
      tryParseStreamResult()
      ElMessage.success('分析完成')
    },
    onError: (err) => {
      isStreaming.value = false
      ElMessage.error('分析失败: ' + err.message)
    }
  })
}

// 尝试解析流内容中的JSON结果
function tryParseStreamResult() {
  try {
    // 尝试在流内容中查找JSON
    const jsonMatch = streamContent.value.match(/\{[\s\S]*"extracted"[\s\S]*\}/)
    if (jsonMatch) {
      analysisResult.value = JSON.parse(jsonMatch[0])
    }
  } catch (e) {
    console.log('解析流内容失败', e)
  }
}

// 切换建议展开
function toggleSuggestion(id) {
  const idx = expandedSuggestions.value.indexOf(id)
  if (idx > -1) {
    expandedSuggestions.value.splice(idx, 1)
  } else {
    expandedSuggestions.value.push(id)
  }
}

// 获取类型颜色
function getTypeColor(type) {
  const colors = {
    '铺垫': 'info',
    '冲突': 'danger',
    '反转': 'warning',
    '高潮': 'primary',
    '过渡': '',
    '收尾': 'success'
  }
  return colors[type] || 'info'
}

// 应用单个建议
function applySuggestion(suggestion) {
  ElMessageBox.confirm(`确定应用事件"${suggestion.title}"到大纲？`, '应用建议', {
    confirmButtonText: '确定',
    cancelButtonText: '取消'
  }).then(async () => {
    try {
      await api.post('/ai/save-outline-events', {
        novel_id: novelId.value,
        chapter_id: chapterId.value,
        events: [{
          title: suggestion.title,
          description: suggestion.description,
          participants: suggestion.participants,
          level: config.granularity === 'chapter' ? 'chapter' : 'scene'
        }]
      })
      ElMessage.success('已添加到大纲')
    } catch (err) {
      ElMessage.error('添加失败')
    }
  }).catch(() => {})
}

// 预览建议
function previewSuggestion(suggestion) {
  previewData.value = suggestion
  previewDialogVisible.value = true
}

// 应用预览建议
function applyPreviewSuggestion() {
  if (previewData.value) {
    applySuggestion(previewData.value)
  }
  previewDialogVisible.value = false
}

// 应用全部建议
function applyAllSuggestions() {
  if (!analysisResult.value?.suggestions?.length) return
  
  ElMessageBox.confirm(`确定应用全部 ${analysisResult.value.suggestions.length} 条建议到大纲？`, '批量应用', {
    confirmButtonText: '确定',
    cancelButtonText: '取消'
  }).then(async () => {
    try {
      const events = analysisResult.value.suggestions.map(s => ({
        title: s.title,
        description: s.description,
        participants: s.participants || [],
        level: config.granularity === 'chapter' ? 'chapter' : 'scene'
      }))
      
      await api.post('/ai/save-outline-events', {
        novel_id: novelId.value,
        chapter_id: chapterId.value,
        events
      })
      
      ElMessage.success(`已添加 ${events.length} 个事件到大纲`)
    } catch (err) {
      ElMessage.error('批量添加失败')
    }
  }).catch(() => {})
}

// 导出分析报告
function exportAnalysis() {
  if (!analysisResult.value) return
  
  const report = {
    input: inputText.value,
    timestamp: new Date().toISOString(),
    extracted: analysisResult.value.extracted,
    suggestions: analysisResult.value.suggestions
  }
  
  const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `analysis-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('已导出分析报告')
}

// 加载历史记录
async function loadHistory() {
  historyDialogVisible.value = true
  try {
    const res = await api.get(`/novels/${novelId.value}/analysis-history`)
    if (res.data.success) {
      historyList.value = res.data.data || []
    }
  } catch (err) {
    console.error('加载历史失败', err)
    // 使用示例数据
    historyList.value = [
      { id: 1, created_at: new Date().toISOString(), content: '示例历史内容...', extracted_count: 4, suggestion_count: 3 }
    ]
  }
}

// 加载历史项
function loadHistoryItem(item) {
  inputText.value = item.content
  if (item.result) {
    analysisResult.value = item.result
  }
  historyDialogVisible.value = false
  ElMessage.success('已加载历史记录')
}

// 格式化时间
function formatTime(time) {
  if (!time) return ''
  const d = new Date(time)
  return d.toLocaleString('zh-CN')
}
</script>

<style scoped>
.step-analysis-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
}

/* 头部 */
.analysis-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

/* 主体 */
.analysis-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 输入区 */
.input-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-label {
  font-weight: 600;
  font-size: 14px;
}

.input-actions {
  display: flex;
  gap: 8px;
}

.quick-actions {
  display: flex;
  gap: 12px;
}

/* 实时输出 */
.realtime-output {
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 16px;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.pulse-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  background: #67C23A;
  border-radius: 50%;
  margin-right: 6px;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.output-content {
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
  padding: 12px;
  background: var(--bg-primary);
  border-radius: 4px;
}

.streaming-cursor {
  display: inline-block;
  color: var(--brand-primary);
  font-weight: bold;
  animation: blink 0.8s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 配置区 */
.config-section {
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 16px;
}

.section-title {
  font-weight: 600;
  margin-bottom: 16px;
  font-size: 14px;
}

.config-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.config-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* 结果区 */
.result-area {
  width: 400px;
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-color);
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-section {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

/* 元素卡片 */
.element-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.element-card {
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.card-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.card-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.card-items {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 建议列表 */
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 400px;
  overflow-y: auto;
}

.suggestion-item {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}

.suggestion-item.expanded {
  border-color: var(--brand-primary);
}

.item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.item-header:hover {
  background: var(--bg-secondary);
}

.item-title {
  flex: 1;
  font-weight: 500;
}

.expand-icon {
  transition: transform 0.3s;
}

.item-body {
  padding: 0 12px 12px;
  font-size: 13px;
  line-height: 1.6;
}

.item-body .label {
  color: var(--text-secondary);
  font-weight: 500;
}

.item-description {
  margin-bottom: 12px;
}

.item-participants {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.item-reasoning {
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.item-followups ul {
  margin: 8px 0;
  padding-left: 20px;
}

.item-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

/* 结果操作 */
.result-actions {
  display: flex;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

/* 预览 */
.preview-content {
  max-height: 60vh;
  overflow-y: auto;
}

.preview-content h3 {
  margin: 0 0 12px;
}

.preview-type {
  margin-bottom: 16px;
}

.preview-section {
  margin-bottom: 16px;
}

.preview-section p {
  margin: 8px 0 0;
  line-height: 1.6;
}

.preview-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 8px;
}

/* 历史记录 */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  padding: 16px;
  background: var(--bg-primary);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.history-item:hover {
  background: var(--bg-secondary);
}

.history-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.history-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.history-preview {
  margin-bottom: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.history-stats {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 响应式 */
@media (max-width: 1024px) {
  .result-area {
    width: 340px;
  }
  
  .element-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .analysis-main {
    flex-direction: column;
  }
  
  .result-area {
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--border-color);
  }
}
</style>
