<template>
  <div class="writing-workspace" :data-theme="pageTheme">
    <!-- 左栏：章节导航 -->
    <ChapterSidebar
      :chapters="chapters"
      :currentChapterId="currentChapter?.id"
      :novelTitle="novel.title"
      :collapsed="sidebarCollapsed"
      @select-chapter="switchChapter"
      @add-chapter="openNewChapter"
      @go-back="goBack"
    />

    <!-- 中栏：编辑器 -->
    <div class="workspace-center">
      <!-- 顶部章节标题栏 -->
      <div class="chapter-header">
        <input
          v-model="chapterTitle"
          class="chapter-title-input"
          placeholder="章节标题"
          @blur="saveCurrentChapter"
        />
        <div class="header-actions">
          <select v-model="pageTheme" class="theme-select" title="页面主题">
            <option value="dark">墨渊</option>
            <option value="light">纸韵</option>
            <option value="eyecare">宣纸</option>
          </select>
        </div>
      </div>

      <!-- 编辑器 -->
      <ChapterEditor
        ref="editorRef"
        v-model="chapterContent"
        :currentTheme="editorTheme"
        :showAiLegend="true"
        @save="handleEditorSave"
        @selection-change="handleSelectionChange"
        @content-change="handleContentChange"
      />

      <!-- 底栏：故事信息工具条 -->
      <StoryInfoBar
        :charCount="charCount"
        :saveStatus="editorSaveStatus"
        :novelId="novelId"
        :currentTheme="editorTheme"
        @update:currentTheme="editorTheme = $event"
      />
    </div>

    <!-- 右栏：AI对话面板 -->
    <AiChatPanel
      :collapsed="chatCollapsed"
      :novelId="novelId"
      :chapterId="currentChapter?.id"
      :selectedText="selectedText"
      :editorContent="chapterContent"
      @update:collapsed="chatCollapsed = $event"
      @insert-to-editor="handleAiInsert"
      @replace-selection="handleAiReplace"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { setTheme as setDocTheme, getTheme as getDocTheme } from '@/composables/useTheme'
import { useRoute, useRouter } from 'vue-router'
// ElMessage removed
import { getNovel } from '@/api/modules/novel'
import { getChapters, getChapter, createChapter } from '@/api/modules/chapter'
import api from '@/api'
import ChapterSidebar from '@/components/ChapterSidebar.vue'
import ChapterEditor from '@/components/ChapterEditor.vue'
import AiChatPanel from '@/components/AiChatPanel.vue'
import StoryInfoBar from '@/components/StoryInfoBar.vue'

const route = useRoute()
const router = useRouter()

const novelId = computed(() => route.params.novelId)
const chapterId = computed(() => route.params.chapterId)

// 数据
const novel = ref({})
const chapters = ref([])
const currentChapter = ref(null)
const chapterTitle = ref('')
const chapterContent = ref('')

// UI状态
const sidebarCollapsed = ref(false)
const chatCollapsed = ref(false)
const editorTheme = ref('typora')
const pageTheme = ref('dark')
const editorSaveStatus = ref('saved')
const selectedText = ref('')
const editorRef = ref(null)
const previousDocTheme = ref('')

// 同步页面主题到 document.documentElement，使 CSS 变量生效
watch(pageTheme, (val) => {
  setDocTheme(val)
})

const charCount = computed(() => {
  if (!chapterContent.value) return 0
  return chapterContent.value.replace(/<[^>]*>/g, '').replace(/\s/g, '').length
})

// 加载数据
const loadNovel = async () => {
  try {
    const res = await getNovel(novelId.value)
    novel.value = res.data || res
  } catch (err) {
    console.error
  }
}

const loadChapters = async () => {
  try {
    const res = await getChapters(novelId.value)
    chapters.value = res.data?.items || res.data || res || []
  } catch (err) {
    chapters.value = []
  }
}

const loadChapter = async (id) => {
  try {
    const res = await getChapter(id)
    const data = res.data || res
    currentChapter.value = data
    chapterTitle.value = data.title || ''
    chapterContent.value = data.content || ''
    document.title = `${data.title || '写作'} - ${novel.value.title || '十方书社'}`
  } catch (err) {
    console.error
  }
}

// 切换章节
const switchChapter = async (chapter) => {
  // 先保存当前章节
  await saveCurrentChapter()
  // 跳转路由
  router.push(`/write/${novelId.value}/${chapter.id}`)
}

// 新建章节
const openNewChapter = async () => {
  try {
    const res = await createChapter(novelId.value, {
      title: `第${chapters.value.length + 1}章`,
      order: chapters.value.length + 1
    })
    const newChapter = res.data || res
    console.log
    await loadChapters()
    router.push(`/write/${novelId.value}/${newChapter.id}`)
  } catch (err) {
    console.error
  }
}

// 保存
const saveCurrentChapter = async () => {
  if (!currentChapter.value || !chapterTitle.value.trim()) return
  try {
    editorSaveStatus.value = 'saving'
    await api.put(`/chapters/${currentChapter.value.id}`, {
      title: chapterTitle.value,
      content: chapterContent.value
    })
    editorSaveStatus.value = 'saved'
    // 更新列表中的标题
    const idx = chapters.value.findIndex(c => c.id === currentChapter.value.id)
    if (idx !== -1) {
      chapters.value[idx].title = chapterTitle.value
      chapters.value[idx].content = chapterContent.value
    }
  } catch (err) {
    editorSaveStatus.value = 'unsaved'
    console.error('保存失败:', err)
  }
}

const handleEditorSave = (html) => {
  chapterContent.value = html
  saveCurrentChapter()
}

const handleSelectionChange = (text) => {
  selectedText.value = text
}

const handleContentChange = (html) => {
  chapterContent.value = html
}

// AI面板操作
const handleAiInsert = (content) => {
  editorRef.value?.insertContent(content)
}

const handleAiReplace = (content) => {
  editorRef.value?.replaceSelection(content)
}

// 返回
const goBack = () => {
  saveCurrentChapter()
  router.push(`/home/novels/${novelId.value}`)
}

// 键盘快捷键
const handleKeydown = (e) => {
  // Ctrl+Shift+P 切换AI面板
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'P') {
    e.preventDefault()
    chatCollapsed.value = !chatCollapsed.value
  }
  // Ctrl+Shift+S 切换侧边栏
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'S') {
    e.preventDefault()
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
  // Esc 关闭AI面板
  if (e.key === 'Escape' && !chatCollapsed.value) {
    chatCollapsed.value = true
  }
}

// 路由变化加载章节
watch(chapterId, (newId) => {
  if (newId) loadChapter(newId)
}, { immediate: false })

onMounted(async () => {
  window.addEventListener('keydown', handleKeydown)
  // 保存原主题并应用写作工作台主题
  previousDocTheme.value = getDocTheme() || 'dark'
  setDocTheme(pageTheme.value)
  await loadNovel()
  await loadChapters()
  if (chapterId.value) {
    await loadChapter(chapterId.value)
  } else if (chapters.value.length) {
    router.replace(`/write/${novelId.value}/${chapters.value[0].id}`)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
  saveCurrentChapter()
  // 恢复原来的页面主题
  if (previousDocTheme.value) {
    setDocTheme(previousDocTheme.value)
  }
})
</script>

<style scoped>
.writing-workspace {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: var(--bg-primary, #0D0D12);
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.workspace-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

/* 章节标题栏 */
.chapter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: var(--bg-secondary, #16161E);
  border-bottom: 1px solid var(--border-color, #2A2A36);
  flex-shrink: 0;
  gap: 12px;
}

.chapter-title-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--text-primary, #E4E4E8);
  font-size: 16px;
  font-weight: 600;
  font-family: var(--font-body), sans-serif;
  outline: none;
  padding: 4px 0;
}
.chapter-title-input::placeholder { color: var(--text-placeholder, #5A5A6E); }
.chapter-title-input:focus { border-bottom: 1px solid var(--brand-primary, #6C8EEF); }

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.theme-select {
  padding: 3px 8px;
  background: var(--bg-input, #1A1A24);
  color: var(--text-secondary, #8B8B9E);
  border: 1px solid var(--border-color, #2A2A36);
  border-radius: 4px;
  font-size: 11px;
  outline: none;
  cursor: pointer;
}
.theme-select:focus { border-color: var(--brand-primary); }

/* 移动端 */
@media (max-width: 768px) {
  .writing-workspace { flex-direction: column; }
  .chapter-header { padding: 6px 12px; }
  .chapter-title-input { font-size: 14px; }
}
</style>
