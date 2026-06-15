import { ref, computed } from 'vue'
import api from '@/api'

/**
 * 人机共创流程状态管理
 * 4步流程：灵感输入 → AI分析 → 事件组合 → AI填充
 * 已适配真实后端API响应格式
 */
export function useCoCreation() {
  const currentStep = ref(1)

  // Step 1: 灵感输入
  const inspirationText = ref('')
  const novelId = ref(null)
  const chapterId = ref(null)
  const writingStyle = ref('serious')

  // 作品/章节选择器
  const novels = ref([])
  const chapters = ref([])
  const loadingNovels = ref(false)
  const loadingChapters = ref(false)
  const selectedNovelTitle = ref('')
  const selectedChapterTitle = ref('')

  // Step 2: AI分析结果
  const analysisResult = ref(null)
  const selectedEventIds = ref([])
  const analyzing = ref(false)

  // Step 3: 事件组合大纲
  const outlineEvents = ref([])
  const savingOutline = ref(false)

  // Step 4: AI填充
  const filledContent = ref('')
  const filling = ref(false)
  const fillMeta = ref(null)

  const styleOptions = [
    { label: '严肃文学 - 细腻、深沉、富有哲理', value: 'serious' },
    { label: '轻松幽默 - 诙谐、活泼、接地气', value: 'humor' },
    { label: '热血战斗 - 激情、热血、战斗场面', value: 'action' },
    { label: '悬疑推理 - 紧张、烧脑、逻辑严密', value: 'mystery' },
    { label: '浪漫言情 - 甜蜜、细腻、情感丰富', value: 'romance' },
    { label: '科幻未来 - 前沿、想象、科技感', value: 'scifi' },
  ]

  // 事件类型映射 — 适配后端返回的中文类型 + 兼容英文key
  const eventTypeMap = {
    '主线': { label: '主线', color: '#409eff' },
    '支线': { label: '支线', color: '#67c23a' },
    '转折': { label: '转折', color: '#e6a23c' },
    '冲突': { label: '冲突', color: '#f56c6c' },
    '设定': { label: '设定', color: '#909399' },
    plot: { label: '情节', color: '#409eff' },
    character: { label: '人物', color: '#67c23a' },
    conflict: { label: '冲突', color: '#f56c6c' },
    setting: { label: '设定', color: '#e6a23c' },
  }

  const suggestions = computed(() => {
    if (!analysisResult.value) return []
    return analysisResult.value.suggestions || []
  })

  const selectedEvents = computed(() => {
    return suggestions.value.filter(e => selectedEventIds.value.includes(e.id))
  })

  const extractedInfo = computed(() => {
    if (!analysisResult.value?.extracted) return null
    return analysisResult.value.extracted
  })

  const inspirationWordCount = computed(() => {
    return inspirationText.value.replace(/\s/g, '').length
  })

  const filledWordCount = computed(() => {
    return filledContent.value.replace(/\s/g, '').length
  })

  const canProceed = computed(() => {
    switch (currentStep.value) {
      case 1: return inspirationText.value.trim().length > 0
      case 2: return selectedEventIds.value.length > 0
      case 3: return outlineEvents.value.length > 0
      case 4: return filledContent.value.trim().length > 0
      default: return false
    }
  })

  const steps = [
    { title: '灵感输入', icon: 'Edit', desc: '自由写作' },
    { title: 'AI分析', icon: 'MagicStick', desc: '提取事件' },
    { title: '组合大纲', icon: 'List', desc: '人选事件' },
    { title: 'AI填充', icon: 'Document', desc: '生成正文' },
  ]

  // 加载用户作品列表
  async function loadNovels() {
    loadingNovels.value = true
    try {
      const res = await api.get('/novels')
      novels.value = res.items || []
    } catch (err) {
      console.error('加载作品列表失败', err)
      novels.value = []
    } finally {
      loadingNovels.value = false
    }
  }

  // 加载选中作品的章节列表
  async function loadChapters(novelIdVal) {
    if (!novelIdVal) {
      chapters.value = []
      return
    }
    loadingChapters.value = true
    try {
      const res = await api.get(`/novels/${novelIdVal}/chapters`)
      chapters.value = Array.isArray(res) ? res : []
    } catch (err) {
      console.error('加载章节列表失败', err)
      chapters.value = []
    } finally {
      loadingChapters.value = false
    }
  }

  // 选择作品
  function selectNovel(novel) {
    novelId.value = novel.id
    selectedNovelTitle.value = novel.title
    // 重置章节选择
    chapterId.value = null
    selectedChapterTitle.value = ''
    chapters.value = []
    loadChapters(novel.id)
  }

  // 选择章节
  function selectChapter(chapter) {
    chapterId.value = chapter.id
    selectedChapterTitle.value = chapter.title
  }

  // 清除作品选择
  function clearNovelSelection() {
    novelId.value = null
    chapterId.value = null
    selectedNovelTitle.value = ''
    selectedChapterTitle.value = ''
    chapters.value = []
  }

  // 清除章节选择
  function clearChapterSelection() {
    chapterId.value = null
    selectedChapterTitle.value = ''
  }

  function resetFlow() {
    currentStep.value = 1
    inspirationText.value = ''
    analysisResult.value = null
    selectedEventIds.value = []
    outlineEvents.value = []
    filledContent.value = ''
    fillMeta.value = null
  }

  function goToStep(step) {
    if (step >= 1 && step <= 4) currentStep.value = step
  }

  function nextStep() {
    if (currentStep.value < 4) currentStep.value++
  }

  function prevStep() {
    if (currentStep.value > 1) currentStep.value--
  }

  function toggleEvent(eventId) {
    const idx = selectedEventIds.value.indexOf(eventId)
    if (idx > -1) selectedEventIds.value.splice(idx, 1)
    else selectedEventIds.value.push(eventId)
  }

  function selectAllEvents() {
    selectedEventIds.value = suggestions.value.map(e => e.id)
  }

  function clearSelectedEvents() {
    selectedEventIds.value = []
  }

  function addCustomEvent(title, description) {
    outlineEvents.value.push({
      id: `custom-${Date.now()}`,
      title,
      description,
      type: '主线',
      isCustom: true,
      source: 'user_created'
    })
  }

  function removeOutlineEvent(eventId) {
    outlineEvents.value = outlineEvents.value.filter(e => e.id !== eventId)
  }

  function moveOutlineEvent(fromIndex, toIndex) {
    const item = outlineEvents.value.splice(fromIndex, 1)[0]
    outlineEvents.value.splice(toIndex, 0, item)
  }

  return {
    currentStep, inspirationText, novelId, chapterId, writingStyle,
    novels, chapters, loadingNovels, loadingChapters,
    selectedNovelTitle, selectedChapterTitle,
    analysisResult, selectedEventIds, analyzing,
    outlineEvents, savingOutline,
    filledContent, filling, fillMeta,
    styleOptions, eventTypeMap, steps,
    suggestions, extractedInfo, selectedEvents,
    inspirationWordCount, filledWordCount, canProceed,
    loadNovels, loadChapters, selectNovel, selectChapter,
    clearNovelSelection, clearChapterSelection,
    resetFlow, goToStep, nextStep, prevStep,
    toggleEvent, selectAllEvents, clearSelectedEvents,
    addCustomEvent, removeOutlineEvent, moveOutlineEvent,
  }
}
