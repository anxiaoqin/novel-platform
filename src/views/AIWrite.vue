<template>
  <div class="ai-write-page">
    <h2>AI写作助手</h2>
    
    <div class="main-layout">
      <!-- 左侧：输入区域 -->
      <div class="input-section">
        <el-card>
          <template #header>
            <span>创作输入</span>
          </template>
          
          <!-- 写作模式选择 -->
          <div class="mode-selector">
            <el-radio-group v-model="currentMode" size="large">
              <el-radio-button value="continue">续写</el-radio-button>
              <el-radio-button value="polish">润色</el-radio-button>
              <el-radio-button value="expand">扩写</el-radio-button>
              <el-radio-button value="outline">大纲</el-radio-button>
              <el-radio-button value="summary">摘要</el-radio-button>
            </el-radio-group>
          </div>

          <!-- 模式说明 -->
          <div class="mode-desc">
            <el-tag :type="modeConfig[currentMode].color" size="small">
              {{ modeConfig[currentMode].desc }}
            </el-tag>
          </div>

          <!-- 输入内容 -->
          <el-form label-position="top">
            <el-form-item label="输入内容">
              <el-input 
                v-model="inputText" 
                type="textarea" 
                :rows="6"
                :placeholder="modeConfig[currentMode].placeholder"
              />
            </el-form-item>

            <!-- 扩写模式额外参数 -->
            <el-form-item v-if="currentMode === 'expand'" label="扩写倍数">
              <el-slider v-model="expandTimes" :min="1" :max="5" :step="0.5" show-stops />
              <span class="slider-value">约 {{ Math.round(inputText.length * expandTimes) }} 字</span>
            </el-form-item>

            <!-- 大纲模式参数 -->
            <el-form-item v-if="currentMode === 'outline'" label="章节数量">
              <el-input-number v-model="chapterCount" :min="3" :max="30" />
            </el-form-item>

            <el-form-item label="写作风格">
              <el-select v-model="writingStyle" style="width: 100%">
                <el-option label="严肃文学 - 细腻、深沉、富有哲理" value="serious" />
                <el-option label="轻松幽默 - 诙谐、活泼、接地气" value="humor" />
                <el-option label="热血战斗 - 激情、热血、战斗场面" value="action" />
                <el-option label="悬疑推理 - 紧张、烧脑、逻辑严密" value="mystery" />
                <el-option label="浪漫言情 - 甜蜜、细腻、情感丰富" value="romance" />
                <el-option label="科幻未来 - 前沿、想象、科技感" value="scifi" />
              </el-select>
            </el-form-item>
          </el-form>

          <div class="action-area">
            <el-button type="primary" :loading="generating" @click="handleGenerate" size="large">
              {{ generating ? 'AI创作中...' : '开始创作' }}
            </el-button>
            <el-button @click="handleClear" size="large">清空</el-button>
          </div>
        </el-card>
      </div>

      <!-- 右侧：输出区域 -->
      <div class="output-section">
        <el-card class="output-card">
          <template #header>
            <div class="output-header">
              <span>创作结果</span>
              <div class="output-actions" v-if="outputText">
                <el-button size="small" @click="handleCopy">复制</el-button>
              </div>
            </div>
          </template>
          
          <div v-if="!outputText && !generating" class="empty-output">
            <el-empty description="AI创作结果将显示在这里" :image-size="60" />
          </div>

          <div v-else-if="generating" class="generating">
            <el-icon class="is-loading" :size="32"><Loading /></el-icon>
            <p>AI正在{{ modeConfig[currentMode].action }}，请稍候...</p>
          </div>

          <div v-else class="output-content">
            <div class="word-count-info">字数：{{ outputWordCount }}</div>
            <el-input v-model="outputText" type="textarea" :rows="16" class="output-textarea" />
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import api from '@/api'

const currentMode = ref('continue')
const inputText = ref('')
const expandTimes = ref(2)
const chapterCount = ref(10)
const writingStyle = ref('humor')
const generating = ref(false)
const outputText = ref('')

// 模式配置
const modeConfig = {
  continue: {
    desc: '根据已有内容继续创作，保持文风和节奏',
    placeholder: '请输入开头或已有内容，AI将为你续写...',
    action: '续写中',
    color: 'primary'
  },
  polish: {
    desc: '优化现有文字，提升文笔和表达力',
    placeholder: '粘贴需要润色的段落...',
    action: '润色中',
    color: 'success'
  },
  expand: {
    desc: '对内容进行扩展和深化',
    placeholder: '输入需要扩写的核心内容...',
    action: '扩写中',
    color: 'warning'
  },
  outline: {
    desc: '生成小说章节大纲和结构',
    placeholder: '描述你的小说主题、背景、主角...',
    action: '生成大纲中',
    color: 'info'
  },
  summary: {
    desc: '生成内容摘要和核心要点',
    placeholder: '粘贴需要摘要的长内容...',
    action: '生成摘要中',
    color: ''
  }
}

const outputWordCount = computed(() => {
  return outputText.value.replace(/\s/g, '').length
})

const handleGenerate = async () => {
  if (!inputText.value.trim()) {
    ElMessage.warning('请输入创作内容')
    return
  }

  generating.value = true
  outputText.value = ''

  try {
    const res = await api.post('/ai/generate', {
      mode: currentMode.value,
      prompt: inputText.value,
      style: writingStyle.value
    })
    
    outputText.value = res.generated_text || res.result || '生成完成'
    ElMessage.success('创作完成')
  } catch (err) {
    console.error(err)
    ElMessage.error('生成失败：' + (err.response?.data?.error || err.message))
  } finally {
    generating.value = false
  }
}

const handleCopy = () => {
  navigator.clipboard.writeText(outputText.value)
  ElMessage.success('已复制到剪贴板')
}

const handleClear = () => {
  inputText.value = ''
  outputText.value = ''
}
</script>

<style scoped>
.ai-write-page {
  padding: 20px;
  height: calc(100vh - 120px);
  overflow: hidden;
}

h2 {
  margin: 0 0 20px 0;
}

.main-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  height: calc(100% - 60px);
}

.input-section,
.output-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.mode-selector {
  margin-bottom: 12px;
}

.mode-desc {
  margin-bottom: 16px;
}

.action-area {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.output-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.output-actions {
  display: flex;
  gap: 8px;
}

.empty-output {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.generating {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  color: #666;
}

.output-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.word-count-info {
  font-size: 12px;
  color: #999;
  text-align: right;
}

.output-textarea :deep(textarea) {
  font-size: 14px;
  line-height: 1.8;
}

.slider-value {
  margin-left: 12px;
  color: #409eff;
}

:deep(.el-radio-group) {
  flex-wrap: wrap;
}
</style>
