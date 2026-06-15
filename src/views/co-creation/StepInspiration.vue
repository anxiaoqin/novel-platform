<template>
  <div class="step-inspiration">
    <div class="inspiration-layout">
      <!-- 左侧工具面板 -->
      <div class="left-panel">
        <div class="panel-section">
          <h4 class="panel-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="12" y1="18" x2="12" y2="12"/>
              <line x1="9" y1="15" x2="15" y2="15"/>
            </svg>
            灵感模板
          </h4>
          <div class="template-list">
            <button 
              v-for="tpl in templates" 
              :key="tpl.id"
              class="template-item"
              @click="applyTemplate(tpl)"
            >
              <span class="tpl-icon">{{ tpl.icon }}</span>
              <span class="tpl-name">{{ tpl.name }}</span>
            </button>
          </div>
        </div>

        <div class="panel-section">
          <h4 class="panel-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 20h9"/>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
            </svg>
            历史灵感
          </h4>
          <div class="history-list" v-if="historyList.length > 0">
            <div 
              v-for="item in historyList" 
              :key="item.id"
              class="history-item"
              @click="loadHistory(item)"
            >
              <span class="history-text">{{ item.text.substring(0, 30) }}...</span>
              <span class="history-time">{{ item.time }}</span>
            </div>
          </div>
          <div v-else class="empty-history">
            <span>暂无历史灵感</span>
          </div>
        </div>

        <div class="panel-section">
          <h4 class="panel-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            快捷入口
          </h4>
          <button class="quick-entry" @click="openDocImport">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            导入文档
          </button>
          <button class="quick-entry" @click="openInspirationLib">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            卡文灵感库
          </button>
        </div>
      </div>

      <!-- 中间编辑区 -->
      <div class="center-area">
        <!-- 作品选择器 -->
        <div class="novel-selector">
          <div class="selector-row">
            <div class="selector-item">
              <span class="selector-label">选择作品</span>
              <el-select
                v-model="store.novelId.value"
                placeholder="选择要创作的作品"
                :loading="store.loadingNovels.value"
                clearable
                filterable
                @change="handleNovelChange"
                @clear="handleNovelClear"
                class="dark-select"
              >
                <el-option
                  v-for="novel in store.novels.value"
                  :key="novel.id"
                  :label="`${novel.title}（${novel.genre || '未分类'}）`"
                  :value="novel.id"
                />
              </el-select>
            </div>
            <div class="selector-item" v-if="store.novelId.value">
              <span class="selector-label">选择章节</span>
              <el-select
                v-model="store.chapterId.value"
                placeholder="选择章节"
                :loading="store.loadingChapters.value"
                clearable
                @change="handleChapterChange"
                @clear="handleChapterClear"
                class="dark-select"
              >
                <el-option
                  v-for="ch in store.chapters.value"
                  :key="ch.id"
                  :label="`第${ch.order}章 ${ch.title}`"
                  :value="ch.id"
                />
              </el-select>
            </div>
          </div>
          <div class="selector-hint">
            <el-tag v-if="!store.novelId.value" type="warning" size="small" class="hint-tag">
              未选择作品：AI分析将以纯文本模式运行
            </el-tag>
            <el-tag v-else-if="!store.chapterId.value" type="info" size="small" class="hint-tag">
              已选作品，建议选择章节以便保存
            </el-tag>
            <el-tag v-else type="success" size="small" class="hint-tag">
              已绑定：{{ store.selectedNovelTitle.value }} / {{ store.selectedChapterTitle.value }}
            </el-tag>
          </div>
        </div>

        <!-- 写作区 -->
        <div class="writing-area">
          <div class="editor-wrapper">
            <textarea
              v-model="store.inspirationText.value"
              class="inspiration-textarea"
              placeholder="写下一段脑洞、对话、场景，哪怕只有一句话也可以...

比如：
深夜，一个陌生人推开客栈的门，身上带着奇怪的伤口。
主角觉得此人眼熟，却想不起在哪里见过..."
              @input="handleInput"
            ></textarea>
            <button 
              v-if="!store.inspirationText.value" 
              class="floating-template-btn"
              @click="showTemplatePanel = !showTemplatePanel"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
              </svg>
              灵感模板
            </button>
          </div>

          <!-- 底部字数统计 -->
          <div class="writing-footer">
            <div class="word-count">
              <span class="count-label">字数</span>
              <span class="count-value">{{ store.inspirationWordCount.value }}</span>
            </div>
            <div class="style-select">
              <span class="style-label">写作风格</span>
              <el-select v-model="store.writingStyle.value" size="small" class="dark-select dark-select-small">
                <el-option
                  v-for="opt in store.styleOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </div>
          </div>
        </div>

        <!-- 操作栏 -->
        <div class="action-bar">
          <button class="btn-reset" @click="store.resetFlow()">重置</button>
          <button
            class="btn-primary"
            :class="{ 'btn-active': store.canProceed.value }"
            :disabled="!store.canProceed.value"
            @click="handleSubmit"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            生成事件建议
          </button>
        </div>
      </div>
    </div>

    <!-- 模板弹窗面板 -->
    <div v-if="showTemplatePanel" class="template-panel-overlay" @click.self="showTemplatePanel = false">
      <div class="template-panel">
        <div class="panel-header">
          <h3>灵感模板</h3>
          <button class="panel-close" @click="showTemplatePanel = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="template-grid">
          <div 
            v-for="tpl in templates" 
            :key="tpl.id"
            class="template-card"
            @click="applyTemplate(tpl); showTemplatePanel = false"
          >
            <span class="tpl-icon">{{ tpl.icon }}</span>
            <span class="tpl-name">{{ tpl.name }}</span>
            <span class="tpl-desc">{{ tpl.desc }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCoCreation } from '@/composables/useCoCreation'

const store = useCoCreation()
const showTemplatePanel = ref(false)

const emit = defineEmits(['submit'])

const templates = [
  { id: 1, icon: '🌙', name: '深夜密谈', desc: '营造神秘氛围的夜间场景' },
  { id: 2, icon: '⚔️', name: '冲突对峙', desc: '两人或多方势力的矛盾冲突' },
  { id: 3, icon: '💔', name: '情感转折', desc: '感情线的重要转折点' },
  { id: 4, icon: '🔮', name: '意外发现', desc: '揭示关键信息的意外事件' },
  { id: 5, icon: '🎭', name: '身份揭露', desc: '角色真实身份的曝光' },
  { id: 6, icon: '🌊', name: '危机来临', desc: '高潮前的危机铺垫' },
]

const historyList = ref([])

const handleSubmit = () => {
  emit('submit')
}

const handleNovelChange = (val) => {
  if (val) {
    const novel = store.novels.value.find(n => n.id === val)
    if (novel) store.selectNovel(novel)
  }
}

const handleNovelClear = () => {
  store.clearNovelSelection()
}

const handleChapterChange = (val) => {
  if (val) {
    const ch = store.chapters.value.find(c => c.id === val)
    if (ch) store.selectChapter(ch)
  }
}

const handleChapterClear = () => {
  store.clearChapterSelection()
}

const handleInput = () => {
  // 实时保存到本地存储
  if (store.inspirationText.value) {
    try {
      const history = JSON.parse(localStorage.getItem('inspiration_history') || '[]')
      const newItem = {
        id: Date.now(),
        text: store.inspirationText.value,
        time: new Date().toLocaleString()
      }
      history.unshift(newItem)
      if (history.length > 10) history.pop()
      localStorage.setItem('inspiration_history', JSON.stringify(history))
    } catch (e) {
      console.error(e)
    }
  }
}

const applyTemplate = (tpl) => {
  store.inspirationText.value = tpl.desc
}

const loadHistory = (item) => {
  store.inspirationText.value = item.text
}

const openDocImport = () => {
  // TODO: 打开文档导入功能
}

const openInspirationLib = () => {
  // TODO: 打开卡文灵感库
}

onMounted(() => {
  store.loadNovels()
  // 加载历史记录
  try {
    historyList.value = JSON.parse(localStorage.getItem('inspiration_history') || '[]').slice(0, 5)
  } catch (e) {
    historyList.value = []
  }
})
</script>

<style scoped>
.step-inspiration {
  height: 100%;
}

.inspiration-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

/* 左侧面板 */
.left-panel {
  width: 200px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-section {
  background: var(--bg-card);
  border-radius: 8px;
  padding: 14px;
  border: 1px solid var(--border-color);
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.panel-title svg {
  width: 14px;
  height: 14px;
  color: var(--brand-primary);
}

.template-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.template-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.template-item:hover {
  background: var(--bg-hover);
  border-color: var(--brand-primary);
}

.tpl-icon {
  font-size: 16px;
}

.tpl-name {
  font-size: 12px;
  color: var(--text-secondary);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.history-item {
  padding: 8px;
  background: var(--bg-secondary);
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.history-item:hover {
  background: var(--bg-hover);
}

.history-text {
  display: block;
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-time {
  font-size: 10px;
  color: var(--text-placeholder);
}

.empty-history {
  font-size: 12px;
  color: var(--text-placeholder);
  text-align: center;
  padding: 12px 0;
}

.quick-entry {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 10px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 6px;
}

.quick-entry:last-child {
  margin-bottom: 0;
}

.quick-entry:hover {
  background: var(--bg-hover);
  border-color: var(--brand-primary);
  color: var(--text-primary);
}

.quick-entry svg {
  width: 14px;
  height: 14px;
}

/* 中间编辑区 */
.center-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.novel-selector {
  background: var(--bg-card);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid var(--border-color);
}

.selector-row {
  display: flex;
  gap: 16px;
}

.selector-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.selector-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.selector-hint {
  margin-top: 10px;
}

.hint-tag {
  background: var(--brand-primary-bg) !important;
  border-color: var(--brand-primary) !important;
}

:deep(.dark-select) {
  width: 100%;
}

:deep(.dark-select .el-input__wrapper) {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  box-shadow: none;
}

:deep(.dark-select .el-input__wrapper:hover) {
  border-color: var(--brand-primary);
}

:deep(.dark-select .el-input__inner) {
  color: var(--text-primary);
}

:deep(.dark-select .el-input__inner::placeholder) {
  color: var(--text-placeholder);
}

:deep(.dark-select .el-select__caret) {
  color: var(--text-secondary);
}

:deep(.dark-select-small .el-input__wrapper) {
  background: var(--bg-secondary);
}

/* 写作区 */
.writing-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.editor-wrapper {
  flex: 1;
  position: relative;
  display: flex;
}

.inspiration-textarea {
  flex: 1;
  padding: 20px;
  font-family: var(--font-content);
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-primary);
  background: transparent;
  border: none;
  resize: none;
  outline: none;
}

.inspiration-textarea::placeholder {
  color: var(--text-placeholder);
  line-height: 1.8;
}

.floating-template-btn {
  position: absolute;
  left: 20px;
  bottom: 20px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.floating-template-btn:hover {
  background: var(--brand-primary-bg);
  border-color: var(--brand-primary);
  color: var(--brand-primary);
}

.floating-template-btn svg {
  width: 14px;
  height: 14px;
}

.writing-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.word-count {
  display: flex;
  align-items: center;
  gap: 6px;
}

.count-label {
  font-size: 12px;
  color: var(--text-placeholder);
}

.count-value {
  font-size: 13px;
  color: var(--brand-primary);
  font-weight: 600;
}

.style-select {
  display: flex;
  align-items: center;
  gap: 8px;
}

.style-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* 操作栏 */
.action-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  padding-top: 16px;
}

.btn-reset {
  padding: 10px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-reset:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
  cursor: not-allowed;
  transition: all 0.3s ease;
}

.btn-primary svg {
  width: 16px;
  height: 16px;
}

.btn-active {
  background: var(--brand-primary);
  border-color: var(--brand-primary);
  color: #fff;
  cursor: pointer;
  box-shadow: 0 4px 16px var(--brand-primary-bg);
}

.btn-active:hover {
  background: var(--brand-primary-light);
  box-shadow: 0 6px 20px var(--brand-primary-bg);
}

/* 模板弹窗 */
.template-panel-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.template-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  width: 480px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--text-primary);
}

.panel-close {
  padding: 4px;
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s ease;
}

.panel-close:hover {
  color: var(--text-primary);
}

.panel-close svg {
  width: 18px;
  height: 18px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

.template-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.template-card:hover {
  background: var(--bg-hover);
  border-color: var(--brand-primary);
  transform: translateY(-2px);
}

.template-card .tpl-icon {
  font-size: 28px;
}

.template-card .tpl-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.template-card .tpl-desc {
  font-size: 11px;
  color: var(--text-placeholder);
  line-height: 1.4;
}

/* 移动端适配 */
@media (max-width: 1024px) {
  .left-panel {
    display: none;
  }
}

@media (max-width: 768px) {
  .selector-row {
    flex-direction: column;
    gap: 12px;
  }

  .writing-footer {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  .style-select {
    justify-content: space-between;
  }

  .template-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
