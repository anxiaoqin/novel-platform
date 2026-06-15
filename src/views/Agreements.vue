<template>
  <div class="agreements-container">
    <el-card class="agreements-card">
      <template #header>
        <div class="agreements-header">
          <el-button text @click="goBack">← 返回</el-button>
          <h2>{{ title }}</h2>
        </div>
      </template>
      <div v-if="loading" class="loading">
        <p style="text-align:center;color:var(--text-secondary);">加载中...</p>
      </div>
      <div v-else-if="error" class="error">
        <p style="text-align:center;color:#F56C6C;">{{ error }}</p>
        <div style="text-align:center;"><el-button type="primary" size="small" @click="fetchContent">重试</el-button></div>
      </div>
      <div v-else class="agreements-content" v-html="renderedContent"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const route = useRoute()
const router = useRouter()

const content = ref('')
const loading = ref(true)
const error = ref('')

const typeMap = {
  user_agreement: '十方书社用户服务协议',
  privacy_policy: '十方书社隐私政策',
  ai_disclaimer: '十方书社AIGC版权声明',
  data_contribution: '十方书社用户数据贡献授权协议'
}

const title = computed(() => typeMap[route.params.type] || '协议内容')

function simpleMarkdown(md) {
  if (!md) return ''
  let html = md
    // 转义 HTML 特殊字符
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  // 标题
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>')
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>')
  // 加粗
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  // 引用块
  html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>')
  // 无序列表
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>')
  // 有序列表
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
  // 分隔线
  html = html.replace(/^---$/gm, '<hr/>')
  // 段落（将连续空行分段）
  html = html.replace(/\n\n+/g, '</p><p>')
  // 换行
  html = html.replace(/\n/g, '<br/>')
  // 包裹段落
  html = '<p>' + html + '</p>'
  // 清理空段落
  html = html.replace(/<p>\s*<\/p>/g, '')
  // 合并相邻 blockquote
  html = html.replace(/<\/blockquote><br\/><blockquote>/g, '<br/>')
  // 合并相邻 li
  html = html.replace(/<\/li><br\/><li>/g, '</li><li>')
  return html
}

const renderedContent = computed(() => simpleMarkdown(content.value))

const fetchContent = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await api.get(`/legal/${route.params.type}`)
    content.value = res.content || res.data?.content || ''
  } catch (err) {
    error.value = err.response?.data?.error || '加载失败'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchContent()
})

watch(() => route.params.type, () => {
  fetchContent()
})
</script>

<style scoped>
.agreements-container {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 24px 16px;
  font-family: var(--font-body);
}

.agreements-card {
  max-width: 800px;
  margin: 0 auto;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-card);
}

.agreements-card :deep(.el-card__header) {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
}

.agreements-card :deep(.el-card__body) {
  background: var(--bg-card);
}

.agreements-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.agreements-header h2 {
  margin: 0;
  font-size: 18px;
  color: var(--text-primary);
}

.agreements-content {
  line-height: 1.8;
  font-size: 14px;
  color: var(--text-primary);
  font-family: var(--font-content);
}

.agreements-content :deep(h1) {
  font-size: 20px;
  margin: 20px 0 12px;
  color: var(--text-primary);
}

.agreements-content :deep(h2) {
  font-size: 17px;
  margin: 16px 0 8px;
  color: var(--text-primary);
}

.agreements-content :deep(h3) {
  font-size: 15px;
  margin: 12px 0 6px;
  color: var(--text-primary);
}

.agreements-content :deep(p) {
  margin: 8px 0;
  color: var(--text-primary);
}

.agreements-content :deep(blockquote) {
  border-left: 3px solid var(--brand-primary);
  padding: 8px 16px;
  margin: 12px 0;
  background: var(--brand-primary-bg);
  border-radius: 4px;
  color: var(--text-secondary);
}

.agreements-content :deep(strong) {
  color: var(--text-primary);
}

.agreements-content :deep(li) {
  margin: 4px 0;
  padding-left: 8px;
  color: var(--text-primary);
}

.agreements-content :deep(hr) {
  border: none;
  border-top: 1px solid var(--border-color);
  margin: 16px 0;
}

.loading, .error {
  padding: 24px 0;
}

/* 按钮暗色适配 */
.agreements-card :deep(.el-button--text) {
  color: var(--brand-primary);
}

/* 移动端适配 */
@media (max-width: 480px) {
  .agreements-container {
    padding: 16px 8px;
  }

  .agreements-content :deep(h1) {
    font-size: 18px;
  }

  .agreements-content :deep(h2) {
    font-size: 16px;
  }
}
</style>
