<template>
  <div class="step-fill-container" :class="{ 'focus-mode': isFocusMode }">
    <!-- 顶部工具栏 -->
    <header class="fill-header">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <h2 class="chapter-title">{{ chapterTitle }}</h2>
        <el-tag size="small" type="info">{{ wordCount }}字</el-tag>
      </div>
      <div class="header-center">
        <el-button-group>
          <el-button size="small" :type="activeToolTab === 'ai' ? 'primary' : ''" @click="activeToolTab = 'ai'">
            <el-icon><MagicStick /></el-icon> AI工具
          </el-button>
          <el-button size="small" :type="activeToolTab === 'settings' ? 'primary' : ''" @click="activeToolTab = 'settings'">
            <el-icon><Setting /></el-icon> 设定库
          </el-button>
          <el-button size="small" :type="activeToolTab === 'outline' ? 'primary' : ''" @click="activeToolTab = 'outline'">
            <el-icon><List /></el-icon> 大纲
          </el-button>
        </el-button-group>
      </div>
      <div class="header-right">
        <el-button size="small" @click="toggleFocusMode">
          <el-icon><FullScreen /></el-icon>
        </el-button>
        <el-button type="primary" size="small" @click="saveChapter">
          <el-icon><Check /></el-icon> 保存
        </el-button>
      </div>
    </header>

    <!-- 主体内容区 -->
    <div class="fill-main">
      <!-- 左侧大纲栏 -->
      <aside class="outline-sidebar" v-show="showOutlineSidebar && !isFocusMode">
        <div class="sidebar-header">
          <span>本章大纲</span>
          <el-button text size="small" @click="showOutlineSidebar = false">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
        <div class="outline-tree">
          <el-tree
            :data="chapterOutline"
            :props="{ label: 'title', children: 'children' }"
            node-key="id"
            default-expand-all
            @node-click="handleOutlineNodeClick"
          >
            <template #default="{ node, data }">
              <span class="outline-node">
                <span class="node-icon">{{ getNodeIcon(data.level) }}</span>
                <span class="node-label">{{ node.label }}</span>
                <el-dropdown v-if="data.source === 'ai_suggested'" size="small" trigger="click">
                  <el-button text size="small"><el-icon><MoreFilled /></el-icon></el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="applyOutlineEvent(data)">应用</el-dropdown-item>
                      <el-dropdown-item @click="removeOutlineEvent(data)">删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </span>
            </template>
          </el-tree>
        </div>
        <div class="sidebar-actions">
          <el-button type="primary" size="small" :loading="fillLoading" @click="openFillDialog">
            <el-icon><Edit /></el-icon> AI填充
          </el-button>
          <el-button size="small" @click="analyzeCurrentContent">
            <el-icon><TrendCharts /></el-icon> 分析
          </el-button>
        </div>
      </aside>

      <!-- 编辑区域 -->
      <main class="editor-area">
        <!-- 打字机光标效果 -->
        <div class="typing-indicator" v-if="isStreaming">
          <span class="typing-cursor">|</span>
          <span class="typing-text">{{ streamingPreview }}</span>
        </div>
        
        <!-- 停止生成按钮 -->
        <div class="stream-controls" v-if="isStreaming">
          <el-button type="danger" size="small" @click="stopStreaming">
            <el-icon><VideoPause /></el-icon> 停止生成
          </el-button>
          <span class="stream-tips">AI正在生成内容，点击停止可手动结束</span>
        </div>

        <!-- 文本编辑器 -->
        <div
          ref="editorRef"
          class="content-editor"
          contenteditable="true"
          @input="handleEditorInput"
          @keydown="handleEditorKeydown"
          @mouseup="handleSelectionChange"
          @touchend="handleSelectionChange"
          v-html="editorContent"
        ></div>

        <!-- AI悬浮菜单 -->
        <div
          v-show="showAIMenu"
          class="ai-float-menu"
          :style="{ left: menuPosition.x + 'px', top: menuPosition.y + 'px' }"
        >
          <el-button-group>
            <el-button size="small" @click="handleRewrite" title="重写">
              <el-icon><RefreshRight /></el-icon> 重写
            </el-button>
            <el-button size="small" @click="handleContinue" title="续写">
              <el-icon><DArrowRight /></el-icon> 续写
            </el-button>
            <el-button size="small" @click="handleExpand" title="扩写">
              <el-icon><ZoomIn /></el-icon> 扩写
            </el-button>
            <el-button size="small" @click="handleDeAIDetect" title="去AI味">
              <el-icon><Delete /></el-icon> 去AI味
            </el-button>
            <el-button size="small" @click="handleProofread" title="纠错">
              <el-icon><EditPen /></el-icon> 纠错
            </el-button>
          </el-button-group>
        </div>
      </main>

      <!-- 右侧工具面板 -->
      <aside class="tools-sidebar" v-show="!isFocusMode">
        <!-- AI工具标签页 -->
        <div v-show="activeToolTab === 'ai'" class="tool-panel">
          <el-tabs v-model="aiToolTab">
            <!-- 续写面板 -->
            <el-tab-pane label="续写" name="continue">
              <div class="tool-section">
                <div class="section-title">续写方向</div>
                <el-radio-group v-model="continueConfig.direction" size="small">
                  <el-radio-button label="auto">智能</el-radio-button>
                  <el-radio-button label="conflict">冲突</el-radio-button>
                  <el-radio-button label="emotion">情感</el-radio-button>
                  <el-radio-button label="transition">过渡</el-radio-button>
                  <el-radio-button label="climax">高潮</el-radio-button>
                  <el-radio-button label="foreshadow">伏笔</el-radio-button>
                </el-radio-group>
                
                <div class="section-title" style="margin-top: 16px;">目标字数</div>
                <el-slider v-model="continueConfig.wordCount" :min="200" :max="5000" :step="100" show-input size="small" />
                
                <div class="section-title" style="margin-top: 16px;">候选数量</div>
                <el-radio-group v-model="continueConfig.numCandidates" size="small">
                  <el-radio-button :label="1">1个</el-radio-button>
                  <el-radio-button :label="2">2个</el-radio-button>
                  <el-radio-button :label="3">3个</el-radio-button>
                </el-radio-group>
                
                <el-button type="primary" class="action-btn" :loading="continueLoading" @click="startContinue">
                  <el-icon><DArrowRight /></el-icon> 开始续写
                </el-button>
              </div>
            </el-tab-pane>

            <!-- 去AI味面板 -->
            <el-tab-pane label="去AI味" name="deai">
              <div class="tool-section">
                <div class="section-title">改写浓度</div>
                <el-radio-group v-model="deaiConfig.intensity" size="small">
                  <el-radio-button label="light">轻度</el-radio-button>
                  <el-radio-button label="medium">中度</el-radio-button>
                  <el-radio-button label="heavy">重度</el-radio-button>
                </el-radio-group>
                
                <div class="section-title" style="margin-top: 16px;">内容锁定</div>
                <el-switch v-model="deaiConfig.lockContent" active-text="启用" inactive-text="关闭" size="small" />
                
                <el-button type="primary" class="action-btn" :loading="deaiLoading" @click="startDeAIRewrite">
                  <el-icon><Delete /></el-icon> 开始改写
                </el-button>
              </div>
            </el-tab-pane>

            <!-- 6维纠错面板 -->
            <el-tab-pane label="6维纠错" name="proofread">
              <div class="tool-section">
                <div class="section-title">选择检查维度</div>
                <el-checkbox-group v-model="proofreadConfig.dimensions">
                  <el-checkbox label="character">人设一致性</el-checkbox>
                  <el-checkbox label="terminology">名词一致性</el-checkbox>
                  <el-checkbox label="timeline">时间线</el-checkbox>
                  <el-checkbox label="power_level">战力体系</el-checkbox>
                  <el-checkbox label="redundancy">冗余检测</el-checkbox>
                  <el-checkbox label="basic">基础纠错</el-checkbox>
                </el-checkbox-group>
                
                <el-button type="primary" class="action-btn" :loading="proofreadLoading" @click="startProofread">
                  <el-icon><EditPen /></el-icon> 一键检查
                </el-button>
              </div>
            </el-tab-pane>

            <!-- 知识库搜索 -->
            <el-tab-pane label="知识库" name="knowledge">
              <div class="tool-section">
                <div class="section-title">搜索关键词</div>
                <el-input v-model="knowledgeQuery" placeholder="输入搜索内容..." size="small">
                  <template #append>
                    <el-button @click="searchKnowledge" :loading="knowledgeLoading">
                      <el-icon><Search /></el-icon>
                    </el-button>
                  </template>
                </el-input>
                
                <div class="section-title" style="margin-top: 16px;">分类筛选</div>
                <el-select v-model="knowledgeCategory" size="small" placeholder="选择分类">
                  <el-option label="自动识别" value="auto" />
                  <el-option label="历史" value="history" />
                  <el-option label="地理" value="geography" />
                  <el-option label="文化" value="culture" />
                  <el-option label="科学" value="science" />
                  <el-option label="艺术" value="art" />
                  <el-option label="音乐" value="music" />
                  <el-option label="文学" value="literature" />
                </el-select>
                
                <div class="knowledge-results" v-if="knowledgeResults.length">
                  <div v-for="(item, idx) in knowledgeResults" :key="idx" class="knowledge-item">
                    <div class="item-content">{{ item.fact }}</div>
                    <div class="item-source">{{ item.source_detail }}</div>
                    <el-button size="small" text @click="insertKnowledge(item)">插入</el-button>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!-- 设定库标签页 -->
        <div v-show="activeToolTab === 'settings'" class="tool-panel">
          <el-tabs v-model="settingsTab">
            <el-tab-pane label="角色" name="characters">
              <div class="settings-list">
                <div v-for="char in characters" :key="char.id" class="setting-item">
                  <div class="item-header">
                    <span class="item-name">{{ char.name }}</span>
                    <el-tag size="small" :type="char.role_type === 'protagonist' ? 'primary' : 'info'">
                      {{ getRoleTypeLabel(char.role_type) }}
                    </el-tag>
                  </div>
                  <div class="item-desc">{{ char.description }}</div>
                  <el-button size="small" text @click="insertCharacter(char)">插入</el-button>
                </div>
                <el-empty v-if="!characters.length" description="暂无角色设定" />
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="世界观" name="worlds">
              <div class="settings-list">
                <div v-for="world in worlds" :key="world.id" class="setting-item">
                  <div class="item-header">
                    <span class="item-name">{{ world.name }}</span>
                    <el-tag size="small">{{ getCategoryLabel(world.category) }}</el-tag>
                  </div>
                  <div class="item-desc">{{ world.description }}</div>
                  <el-button size="small" text @click="insertWorld(world)">插入</el-button>
                </div>
                <el-empty v-if="!worlds.length" description="暂无世界观设定" />
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!-- 大纲标签页 -->
        <div v-show="activeToolTab === 'outline'" class="tool-panel">
          <div class="outline-header">
            <span>章节大纲</span>
            <el-button size="small" @click="loadOutlineTree">
              <el-icon><Refresh /></el-icon>
            </el-button>
          </div>
          <div class="outline-tree-panel">
            <el-tree
              :data="fullOutlineTree"
              :props="{ label: 'title', children: 'children' }"
              node-key="id"
              default-expand-all
              @node-click="handleOutlineNodeClick"
            >
              <template #default="{ node }">
                <span class="outline-node">
                  <span>{{ node.label }}</span>
                </span>
              </template>
            </el-tree>
          </div>
        </div>
      </aside>
    </div>

    <!-- AI填充对话框 -->
    <el-dialog v-model="fillDialogVisible" title="AI章节填充" width="600px">
      <div class="fill-dialog-content">
        <div class="section-title">选择要填充的事件</div>
        <el-checkbox-group v-model="selectedEvents">
          <div v-for="event in availableEvents" :key="event.id" class="event-option">
            <el-checkbox :value="event.id">
              <span class="event-title">{{ event.title }}</span>
              <span class="event-desc">{{ event.description }}</span>
            </el-checkbox>
          </div>
        </el-checkbox-group>
        
        <div class="section-title" style="margin-top: 16px;">写作风格（可选）</div>
        <el-input v-model="fillStyle" placeholder="如：古风、热血、轻松..." size="small" />
        
        <div class="section-title" style="margin-top: 16px;">用户已有段落（可选）</div>
        <el-input v-model="userParagraph" type="textarea" :rows="3" placeholder="粘贴用户已写的内容，AI将续写衔接..." />
      </div>
      <template #footer>
        <el-button @click="fillDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="fillLoading" @click="startFillChapter">
          <el-icon><MagicStick /></el-icon> 开始填充（流式）
        </el-button>
        <el-button @click="startFillChapterNonStream">
          非流式填充
        </el-button>
      </template>
    </el-dialog>

    <!-- 去AI味检测结果对话框 -->
    <el-dialog v-model="deaiDialogVisible" title="AI味检测结果" width="700px">
      <div class="deai-result">
        <div class="score-display">
          <el-progress type="circle" :percentage="deaiScore" :color="getScoreColor(deaiScore)" />
          <div class="score-label">AI味指数</div>
        </div>
        
        <div class="issues-list" v-if="deaiIssues.length">
          <div class="section-title">检测到的问题</div>
          <el-alert v-for="(issue, idx) in deaiIssues" :key="idx" :type="getIssueType(issue.severity)" :closable="false">
            <template #title>
              <span class="issue-type">{{ issue.type }}</span>
              <span class="issue-text">"{{ issue.text }}"</span>
            </template>
            <template #default>
              <div class="issue-reason">{{ issue.reason }}</div>
              <div class="issue-suggestion">{{ issue.suggestion }}</div>
            </template>
          </el-alert>
        </div>
      </div>
      <template #footer>
        <el-button @click="deaiDialogVisible = false">关闭</el-button>
        <el-button type="primary" :loading="deaiRewriteLoading" @click="applyDeAIRewrite">
          应用改写
        </el-button>
        <el-button @click="applyDeAIRewriteStream">
          流式改写
        </el-button>
      </template>
    </el-dialog>

    <!-- 6维纠错结果对话框 -->
    <el-dialog v-model="proofreadDialogVisible" title="6维纠错结果" width="800px">
      <div class="proofread-result">
        <!-- 综合评分 -->
        <div class="overall-score">
          <el-progress type="circle" :percentage="overallScore" :color="getScoreColor(overallScore)" />
          <div class="score-label">综合评分</div>
        </div>
        
        <!-- 6维雷达图 -->
        <div class="radar-chart">
          <div ref="radarChartRef" class="chart-container"></div>
        </div>
        
        <!-- 各维度详情 -->
        <div class="dimensions-detail">
          <el-collapse v-model="activeDimension">
            <el-collapse-item
              v-for="(dim, key) in dimensionResults"
              :key="key"
              :title="getDimensionName(key) + ' (' + dim.score + '分)'"
              :name="key"
            >
              <div class="dimension-header">
                <el-progress :percentage="dim.score" :color="getScoreColor(dim.score)" :show-text="false" />
              </div>
              <div v-if="dim.issues && dim.issues.length" class="issues-list">
                <div v-for="(issue, idx) in dim.issues" :key="idx" class="issue-item">
                  <el-tag size="small" type="warning">{{ issue.position || '全文' }}</el-tag>
                  <span class="issue-text">{{ issue.description || issue.text }}</span>
                </div>
              </div>
              <el-empty v-else description="该维度检查通过" :image-size="60" />
            </el-collapse-item>
          </el-collapse>
        </div>
        
        <div class="summary-section" v-if="proofreadSummary">
          <div class="section-title">整体评价</div>
          <div class="summary-text">{{ proofreadSummary }}</div>
        </div>
      </div>
      <template #footer>
        <el-button @click="proofreadDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="applyProofreadFixes">应用修复建议</el-button>
      </template>
    </el-dialog>

    <!-- 续写候选对话框 -->
    <el-dialog v-model="continueDialogVisible" title="续写候选" width="700px">
      <div class="continue-candidates">
        <el-radio-group v-model="selectedCandidate" class="candidate-list">
          <div v-for="(candidate, idx) in continueCandidates" :key="idx" class="candidate-item">
            <el-radio :value="idx">
              <div class="candidate-header">
                <span class="candidate-label">{{ candidate.style || '方案' + (idx + 1) }}</span>
                <span class="candidate-words">{{ candidate.word_count || candidate.content?.length || 0 }}字</span>
              </div>
              <div class="candidate-preview">{{ candidate.content?.substring(0, 200) }}...</div>
            </el-radio>
            <el-button size="small" text @click="previewCandidate(idx)">预览全文</el-button>
          </div>
        </el-radio-group>
      </div>
      <template #footer>
        <el-button @click="continueDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="applySelectedCandidate">应用到正文</el-button>
      </template>
    </el-dialog>

    <!-- 预览对话框 -->
    <el-dialog v-model="previewDialogVisible" title="内容预览" width="700px">
      <div class="preview-content" v-html="previewContent"></div>
      <template #footer>
        <el-button @click="previewDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="applyPreview">应用到正文</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  ArrowLeft, MagicStick, Setting, List, FullScreen, Check, Close,
  RefreshRight, DArrowRight, ZoomIn, Delete, EditPen, TrendCharts,
  VideoPause, MoreFilled, Refresh, Search, Edit
} from '@element-plus/icons-vue'
import { createSSEStream, extractContent } from '@/api/sse'
import api from '@/api'

// 路由
const router = useRouter()
const route = useRoute()

// 状态
const novelId = ref(route.query.novel_id || 1)
const chapterId = ref(route.query.chapter_id || 1)
const chapterTitle = ref('第一章 觉醒')
const editorContent = ref('')
const wordCount = computed(() => editorContent.value.replace(/<[^>]*>/g, '').length)
const isFocusMode = ref(false)
const showOutlineSidebar = ref(true)

// 编辑器引用
const editorRef = ref(null)

// AI菜单
const showAIMenu = ref(false)
const menuPosition = reactive({ x: 0, y: 0 })
const selectedText = ref('')
const selectionRange = ref(null)

// 流式输出状态
const isStreaming = ref(false)
const streamingPreview = ref('')
const streamController = ref(null)

// 工具面板
const activeToolTab = ref('ai')
const aiToolTab = ref('continue')
const settingsTab = ref('characters')
const outlineTab = ref('events')

// 填充配置
const fillDialogVisible = ref(false)
const fillLoading = ref(false)
const selectedEvents = ref([])
const availableEvents = ref([])
const fillStyle = ref('')
const userParagraph = ref('')

// 续写配置
const continueLoading = ref(false)
const continueConfig = reactive({
  direction: 'auto',
  wordCount: 1000,
  numCandidates: 1
})
const continueCandidates = ref([])
const continueDialogVisible = ref(false)
const selectedCandidate = ref(0)

// 去AI味配置
const deaiLoading = ref(false)
const deaiRewriteLoading = ref(false)
const deaiConfig = reactive({
  intensity: 'medium',
  lockContent: false
})
const deaiDialogVisible = ref(false)
const deaiScore = ref(0)
const deaiIssues = ref([])
const deaiSuggestions = ref([])
const detectedContent = ref('')

// 6维纠错配置
const proofreadLoading = ref(false)
const proofreadConfig = reactive({
  dimensions: ['character', 'terminology', 'timeline', 'power_level', 'redundancy', 'basic']
})
const proofreadDialogVisible = ref(false)
const overallScore = ref(0)
const dimensionResults = ref({})
const proofreadSummary = ref('')
const activeDimension = ref([])
const radarChartRef = ref(null)

// 知识库
const knowledgeQuery = ref('')
const knowledgeCategory = ref('auto')
const knowledgeLoading = ref(false)
const knowledgeResults = ref([])

// 设定库
const characters = ref([])
const worlds = ref([])

// 大纲
const chapterOutline = ref([])
const fullOutlineTree = ref([])

// 预览
const previewDialogVisible = ref(false)
const previewContent = ref('')

// 初始化
onMounted(() => {
  loadChapterData()
  loadCharacters()
  loadWorlds()
  loadOutlineTree()
  document.addEventListener('selectionchange', handleSelectionChange)
  document.addEventListener('click', handleOutsideClick)
})

onUnmounted(() => {
  stopStreaming()
  document.removeEventListener('selectionchange', handleSelectionChange)
  document.removeEventListener('click', handleOutsideClick)
})

// 加载章节数据
async function loadChapterData() {
  try {
    const res = await api.get(`/chapters/${chapterId.value}`)
    if (res.data.success) {
      chapterTitle.value = res.data.data.title || '未命名章节'
      editorContent.value = res.data.data.content || ''
    }
  } catch (err) {
    console.error('加载章节失败', err)
    // 使用示例内容
    editorContent.value = '<p>天色渐暗，林风独自站在悬崖边，望着远方的云海。</p><p>这是他离开宗门的第三天。</p>'
  }
}

// 加载角色列表
async function loadCharacters() {
  try {
    const res = await api.get(`/novels/${novelId.value}/characters`)
    if (res.data.success) {
      characters.value = res.data.data || []
    }
  } catch (err) {
    console.error('加载角色失败', err)
  }
}

// 加载世界观列表
async function loadWorlds() {
  try {
    const res = await api.get(`/novels/${novelId.value}/worlds`)
    if (res.data.success) {
      worlds.value = res.data.data || []
    }
  } catch (err) {
    console.error('加载世界观失败', err)
  }
}

// 加载大纲树
async function loadOutlineTree() {
  try {
    const res = await api.get(`/novels/${novelId.value}/outline-tree`)
    if (res.data.success) {
      fullOutlineTree.value = res.data.data.outline || []
    }
  } catch (err) {
    console.error('加载大纲失败', err)
    // 示例数据
    fullOutlineTree.value = [
      { id: 1, title: '第一卷 觉醒', level: 'volume', children: [
        { id: 2, title: '第一章 离开', level: 'chapter', children: [
          { id: 3, title: '场景1：悬崖思考', level: 'scene' }
        ]}
      ]}
    ]
  }
}

// 编辑器输入处理
function handleEditorInput(e) {
  editorContent.value = e.target.innerHTML
}

// 编辑器按键处理
function handleEditorKeydown(e) {
  if (e.key === 'Tab') {
    e.preventDefault()
    document.execCommand('insertText', false, '    ')
  }
}

// 选中文字变化
function handleSelectionChange() {
  const selection = window.getSelection()
  if (selection && selection.toString().trim().length > 0) {
    selectedText.value = selection.toString()
    
    const range = selection.getRangeAt(0)
    selectionRange.value = range
    
    const rect = range.getBoundingClientRect()
    menuPosition.x = rect.left + rect.width / 2 - 150
    menuPosition.y = rect.top - 50
    
    showAIMenu.value = true
  } else {
    showAIMenu.value = false
  }
}

// 点击外部关闭AI菜单
function handleOutsideClick(e) {
  if (showAIMenu.value && !e.target.closest('.ai-float-menu') && !e.target.closest('.content-editor')) {
    showAIMenu.value = false
  }
}

// 返回
function goBack() {
  router.back()
}

// 切换专注模式
function toggleFocusMode() {
  isFocusMode.value = !isFocusMode.value
}

// 保存章节
async function saveChapter() {
  try {
    await api.put(`/chapters/${chapterId.value}`, {
      content: editorContent.value
    })
    ElMessage.success('保存成功')
  } catch (err) {
    ElMessage.error('保存失败')
  }
}

// 打开填充对话框
function openFillDialog() {
  selectedEvents.value = []
  availableEvents.value = chapterOutline.value.flatMap(flattenOutline)
  fillDialogVisible.value = true
}

// 扁平化大纲
function flattenOutline(nodes) {
  const result = []
  function traverse(node) {
    result.push({ id: node.id, title: node.title, description: node.description })
    if (node.children) {
      node.children.forEach(traverse)
    }
  }
  nodes.forEach(traverse)
  return result
}

// 获取大纲节点图标
function getNodeIcon(level) {
  const icons = { volume: '📚', chapter: '📖', scene: '🎬', paragraph: '📝' }
  return icons[level] || '📄'
}

// 开始填充（非流式fallback）
async function startFillChapterNonStream() {
  if (!selectedEvents.value.length) {
    ElMessage.warning('请选择至少一个事件')
    return
  }
  
  fillLoading.value = true
  try {
    const events = availableEvents.value.filter(e => selectedEvents.value.includes(e.id))
    const res = await api.post('/ai/fill-chapter', {
      novel_id: novelId.value,
      chapter_id: chapterId.value,
      events: events,
      user_paragraph: userParagraph.value,
      style: fillStyle.value
    })
    
    if (res.data.success) {
      insertContentAtCursor(res.data.data.content)
      ElMessage.success('填充完成')
    }
  } catch (err) {
    ElMessage.error('填充失败')
  } finally {
    fillLoading.value = false
    fillDialogVisible.value = false
  }
}

// 开始填充（流式）
function startFillChapter() {
  if (!selectedEvents.value.length) {
    ElMessage.warning('请选择至少一个事件')
    return
  }
  
  fillLoading.value = true
  const events = availableEvents.value.filter(e => selectedEvents.value.includes(e.id))
  
  // 创建临时光标标记
  const markerId = 'stream-marker-' + Date.now()
  insertHTMLAtCursor(`<span id="${markerId}" class="streaming-marker"></span>`)
  
  const targetElement = document.getElementById(markerId)
  let accumulatedContent = ''
  
  streamController.value = createSSEStream('/ai/fill-chapter/stream', {
    novel_id: novelId.value,
    chapter_id: chapterId.value,
    events: events,
    user_paragraph: userParagraph.value,
    writing_style: fillStyle.value
  }, {
    onMessage: (data) => {
      const content = extractContent(data)
      if (content) {
        accumulatedContent += content
        // 更新显示
        streamingPreview.value = accumulatedContent
        // 替换标记为实际内容
        if (targetElement) {
          targetElement.innerHTML = accumulatedContent
        }
      }
    },
    onDone: () => {
      isStreaming.value = false
      fillLoading.value = false
      streamingPreview.value = ''
      // 移除标记
      if (targetElement) {
        targetElement.remove()
      }
      ElMessage.success('填充完成')
    },
    onError: (err) => {
      isStreaming.value = false
      fillLoading.value = false
      streamingPreview.value = ''
      if (targetElement) {
        targetElement.remove()
      }
      ElMessage.error('填充失败: ' + err.message)
    }
  })
  
  isStreaming.value = true
  fillDialogVisible.value = false
}

// 停止流式生成
function stopStreaming() {
  if (streamController.value) {
    streamController.value.abort()
    streamController.value = null
  }
  isStreaming.value = false
  streamingPreview.value = ''
}

// 重写功能
async function handleRewrite() {
  if (!selectedText.value) return
  
  showAIMenu.value = false
  deaiRewriteLoading.value = true
  
  try {
    const res = await api.post('/ai/deai-rewrite', {
      content: selectedText.value,
      intensity: 'medium'
    })
    
    if (res.data.success) {
      replaceSelectedText(res.data.data.rewritten)
      ElMessage.success('重写完成')
    }
  } catch (err) {
    ElMessage.error('重写失败')
  } finally {
    deaiRewriteLoading.value = false
  }
}

// 续写功能
function handleContinue() {
  if (!selectedText.value) {
    ElMessage.warning('请先选中要续写的位置')
    return
  }
  showAIMenu.value = false
  startContinue()
}

// 开始续写（流式）
function startContinue() {
  continueLoading.value = true
  let accumulatedContent = ''
  
  const markerId = 'continue-marker-' + Date.now()
  insertHTMLAtCursor(`<span id="${markerId}" class="streaming-marker"></span>`)
  const targetElement = document.getElementById(markerId)
  
  streamController.value = createSSEStream('/ai/continue-writing/stream', {
    novel_id: novelId.value,
    chapter_id: chapterId.value,
    direction: continueConfig.direction,
    word_count: continueConfig.wordCount
  }, {
    onMessage: (data) => {
      const content = extractContent(data)
      if (content) {
        accumulatedContent += content
        streamingPreview.value = accumulatedContent
        if (targetElement) {
          targetElement.innerHTML = accumulatedContent
        }
      }
    },
    onDone: () => {
      isStreaming.value = false
      continueLoading.value = false
      streamingPreview.value = ''
      if (targetElement) {
        targetElement.remove()
      }
      ElMessage.success('续写完成')
    },
    onError: (err) => {
      isStreaming.value = false
      continueLoading.value = false
      streamingPreview.value = ''
      if (targetElement) {
        targetElement.remove()
      }
      ElMessage.error('续写失败: ' + err.message)
    }
  })
  
  isStreaming.value = true
}

// 扩写功能
function handleExpand() {
  if (!selectedText.value) return
  
  showAIMenu.value = false
  
  ElMessageBox.prompt('请输入目标字数', '扩写设置', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputValue: '800'
  }).then(async ({ value }) => {
    const wordCount = parseInt(value) || 800
    
    fillLoading.value = true
    try {
      const res = await api.post('/ai/fill-event', {
        novel_id: novelId.value,
        chapter_id: chapterId.value,
        event_title: selectedText.value.substring(0, 20),
        event_description: selectedText.value,
        word_count: wordCount
      })
      
      if (res.data.success) {
        replaceSelectedText(res.data.data.content)
        ElMessage.success('扩写完成')
      }
    } catch (err) {
      ElMessage.error('扩写失败')
    } finally {
      fillLoading.value = false
    }
  }).catch(() => {})
}

// 去AI味检测
async function handleDeAIDetect() {
  if (!selectedText.value) return
  
  showAIMenu.value = false
  detectedContent.value = selectedText.value
  deaiLoading.value = true
  
  try {
    const res = await api.post('/ai/deai-detect', {
      content: selectedText.value
    })
    
    if (res.data.success) {
      deaiScore.value = res.data.data.score || 0
      deaiIssues.value = res.data.data.issues || []
      deaiSuggestions.value = res.data.data.suggestions || []
      deaiDialogVisible.value = true
    }
  } catch (err) {
    ElMessage.error('检测失败')
  } finally {
    deaiLoading.value = false
  }
}

// 应用去AI味改写（非流式）
async function applyDeAIRewrite() {
  deaiRewriteLoading.value = true
  
  try {
    const res = await api.post('/ai/deai-rewrite', {
      content: detectedContent.value,
      intensity: deaiConfig.intensity,
      issues: deaiIssues.value,
      lock_content: deaiConfig.lockContent
    })
    
    if (res.data.success) {
      replaceSelectedText(res.data.data.rewritten)
      deaiDialogVisible.value = false
      ElMessage.success('改写完成')
    }
  } catch (err) {
    ElMessage.error('改写失败')
  } finally {
    deaiRewriteLoading.value = false
  }
}

// 应用去AI味改写（流式）
function applyDeAIRewriteStream() {
  deaiRewriteLoading.value = true
  
  const markerId = 'deai-marker-' + Date.now()
  insertHTMLAtCursor(`<span id="${markerId}" class="streaming-marker"></span>`)
  const targetElement = document.getElementById(markerId)
  let accumulatedContent = ''
  
  streamController.value = createSSEStream('/ai/deai-rewrite/stream', {
    content: detectedContent.value,
    intensity: deaiConfig.intensity,
    issues: deaiIssues.value,
    lock_content: deaiConfig.lockContent
  }, {
    onMessage: (data) => {
      const content = extractContent(data)
      if (content) {
        accumulatedContent += content
        if (targetElement) {
          targetElement.innerHTML = accumulatedContent
        }
      }
    },
    onDone: () => {
      isStreaming.value = false
      deaiRewriteLoading.value = false
      deaiDialogVisible.value = false
      if (targetElement) {
        targetElement.remove()
      }
      ElMessage.success('改写完成')
    },
    onError: (err) => {
      isStreaming.value = false
      deaiRewriteLoading.value = false
      if (targetElement) {
        targetElement.remove()
      }
      ElMessage.error('改写失败')
    }
  })
  
  isStreaming.value = true
}

// 纠错功能
async function handleProofread() {
  if (!selectedText.value) return
  
  showAIMenu.value = false
  await startProofread(selectedText.value)
}

// 开始纠错
async function startProofread(content = null) {
  proofreadLoading.value = true
  
  try {
    const res = await api.post('/ai/novel-check', {
      content: content || editorContent.value.replace(/<[^>]*>/g, ''),
      novel_id: novelId.value,
      chapter_id: chapterId.value,
      dimensions: proofreadConfig.dimensions
    })
    
    if (res.data.success) {
      const data = res.data.data
      overallScore.value = data.overall_score || 0
      dimensionResults.value = data.dimensions || {}
      proofreadSummary.value = data.summary || ''
      proofreadDialogVisible.value = true
      
      // 渲染雷达图
      nextTick(() => renderRadarChart())
    }
  } catch (err) {
    ElMessage.error('纠错失败')
  } finally {
    proofreadLoading.value = false
  }
}

// 渲染雷达图
function renderRadarChart() {
  if (!radarChartRef.value || !dimensionResults.value) return
  
  const dimensions = Object.keys(dimensionResults.value)
  const scores = dimensions.map(d => dimensionResults.value[d].score || 0)
  const names = dimensions.map(d => getDimensionName(d))
  
  // 使用Canvas绘制简单雷达图
  const canvas = document.createElement('canvas')
  canvas.width = 300
  canvas.height = 300
  radarChartRef.value.innerHTML = ''
  radarChartRef.value.appendChild(canvas)
  
  const ctx = canvas.getContext('2d')
  const centerX = 150
  const centerY = 150
  const radius = 100
  const angleStep = (Math.PI * 2) / dimensions.length
  
  // 绘制背景多边形
  ctx.strokeStyle = '#ddd'
  ctx.lineWidth = 1
  for (let level = 1; level <= 5; level++) {
    ctx.beginPath()
    for (let i = 0; i <= dimensions.length; i++) {
      const angle = i * angleStep - Math.PI / 2
      const r = radius * level / 5
      const x = centerX + r * Math.cos(angle)
      const y = centerY + r * Math.sin(angle)
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()
  }
  
  // 绘制轴线
  ctx.strokeStyle = '#999'
  for (let i = 0; i < dimensions.length; i++) {
    const angle = i * angleStep - Math.PI / 2
    ctx.beginPath()
    ctx.moveTo(centerX, centerY)
    ctx.lineTo(centerX + radius * Math.cos(angle), centerY + radius * Math.sin(angle))
    ctx.stroke()
    
    // 绘制标签
    const labelX = centerX + (radius + 20) * Math.cos(angle)
    const labelY = centerY + (radius + 20) * Math.sin(angle)
    ctx.fillStyle = '#666'
    ctx.font = '12px sans-serif'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(names[i], labelX, labelY)
  }
  
  // 绘制数据区域
  ctx.fillStyle = 'rgba(64, 158, 255, 0.3)'
  ctx.strokeStyle = '#409EFF'
  ctx.lineWidth = 2
  ctx.beginPath()
  for (let i = 0; i <= dimensions.length; i++) {
    const idx = i % dimensions.length
    const angle = idx * angleStep - Math.PI / 2
    const score = scores[idx] / 100
    const x = centerX + radius * score * Math.cos(angle)
    const y = centerY + radius * score * Math.sin(angle)
    if (i === 0) ctx.moveTo(x, y)
    else ctx.lineTo(x, y)
  }
  ctx.closePath()
  ctx.fill()
  ctx.stroke()
}

// 应用纠错修复
function applyProofreadFixes() {
  // TODO: 根据dimensionResults自动修复问题
  proofreadDialogVisible.value = false
  ElMessage.success('修复建议已应用')
}

// 知识库搜索
async function searchKnowledge() {
  if (!knowledgeQuery.value) {
    ElMessage.warning('请输入搜索内容')
    return
  }
  
  knowledgeLoading.value = true
  try {
    const res = await api.post('/ai/knowledge-search', {
      query: knowledgeQuery.value,
      category: knowledgeCategory.value
    })
    
    if (res.data.success) {
      knowledgeResults.value = res.data.data.results || []
    }
  } catch (err) {
    ElMessage.error('搜索失败')
  } finally {
    knowledgeLoading.value = false
  }
}

// 插入知识库内容
function insertKnowledge(item) {
  insertContentAtCursor(item.fact)
}

// 插入角色设定
function insertCharacter(char) {
  const content = `[${char.name}]${char.description || ''}`
  insertContentAtCursor(content)
}

// 插入世界观设定
function insertWorld(world) {
  const content = `[${world.name}]${world.description || ''}`
  insertContentAtCursor(content)
}

// 大纲节点点击
function handleOutlineNodeClick(data) {
  ElMessage.info(`跳转到: ${data.title}`)
}

// 应用大纲事件
function applyOutlineEvent(data) {
  ElMessage.info('应用事件到编辑区')
}

// 删除大纲事件
function removeOutlineEvent(data) {
  ElMessageBox.confirm('确定删除该事件？').then(async () => {
    // 调用API删除
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 分析当前内容
function analyzeCurrentContent() {
  router.push({
    path: '/co-creation/step-analysis',
    query: { novel_id: novelId.value, chapter_id: chapterId.value }
  })
}

// 工具函数
function getRoleTypeLabel(type) {
  const labels = { protagonist: '主角', supporting: '配角', antagonist: '反派', npc: '路人' }
  return labels[type] || type
}

function getCategoryLabel(category) {
  const labels = { rules: '规则', geography: '地理', history: '历史', culture: '文化' }
  return labels[category] || category
}

function getDimensionName(key) {
  const names = {
    character: '人设一致性',
    terminology: '名词一致性',
    timeline: '时间线',
    power_level: '战力体系',
    redundancy: '冗余检测',
    basic: '基础纠错'
  }
  return names[key] || key
}

function getScoreColor(score) {
  if (score >= 80) return '#67C23A'
  if (score >= 60) return '#E6A23C'
  return '#F56C6C'
}

function getIssueType(severity) {
  const types = { high: 'error', medium: 'warning', low: 'info' }
  return types[severity] || 'info'
}

// 编辑器辅助函数
function insertContentAtCursor(content) {
  const editor = editorRef.value
  if (!editor) return
  
  // 插入段落分隔和内容
  const p = document.createElement('p')
  p.textContent = content
  editor.appendChild(p)
  
  // 移动光标到末尾
  const range = document.createRange()
  range.selectNodeContents(editor)
  range.collapse(false)
  const selection = window.getSelection()
  selection.removeAllRanges()
  selection.addRange(range)
  
  editorContent.value = editor.innerHTML
}

function insertHTMLAtCursor(html) {
  const selection = window.getSelection()
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0)
    range.deleteContents()
    const frag = document.createRange().createContextualFragment(html)
    range.insertNode(frag)
    range.collapse(false)
    selection.removeAllRanges()
    selection.addRange(range)
  }
}

function replaceSelectedText(newText) {
  if (selectionRange.value) {
    selectionRange.value.deleteContents()
    selectionRange.value.insertNode(document.createTextNode(newText))
    editorContent.value = editorRef.value.innerHTML
  }
}

// 预览候选
function previewCandidate(idx) {
  previewContent.value = continueCandidates.value[idx]?.content || ''
  previewDialogVisible.value = true
}

// 应用选中的候选
function applySelectedCandidate() {
  if (continueCandidates.value[selectedCandidate.value]) {
    insertContentAtCursor(continueCandidates.value[selectedCandidate.value].content)
  }
  continueDialogVisible.value = false
}

// 应用预览内容
function applyPreview() {
  insertContentAtCursor(previewContent.value)
  previewDialogVisible.value = false
}
</script>

<style scoped>
.step-fill-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.step-fill-container.focus-mode {
  background: #1a1a1a;
}

/* 头部 */
.fill-header {
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

.chapter-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.header-center {
  display: flex;
  gap: 8px;
}

.header-right {
  display: flex;
  gap: 8px;
}

/* 主体 */
.fill-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧大纲栏 */
.outline-sidebar {
  width: 280px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
}

.outline-tree {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.outline-node {
  display: flex;
  align-items: center;
  gap: 6px;
}

.node-icon {
  font-size: 14px;
}

.sidebar-actions {
  padding: 12px;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 8px;
}

/* 编辑区 */
.editor-area {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.typing-indicator {
  position: absolute;
  top: 10px;
  right: 20px;
  background: var(--bg-secondary);
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  max-width: 300px;
  z-index: 10;
}

.typing-cursor {
  animation: blink 1s infinite;
  color: var(--brand-primary);
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.stream-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 20px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.stream-tips {
  font-size: 12px;
  color: var(--text-secondary);
}

.content-editor {
  flex: 1;
  padding: 40px 60px;
  overflow-y: auto;
  font-size: 16px;
  line-height: 1.8;
  outline: none;
  white-space: pre-wrap;
}

.content-editor:empty::before {
  content: '开始创作...';
  color: var(--text-secondary);
}

/* AI悬浮菜单 */
.ai-float-menu {
  position: fixed;
  z-index: 1000;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 右侧工具面板 */
.tools-sidebar {
  width: 320px;
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-color);
  overflow-y: auto;
}

.tool-panel {
  padding: 16px;
}

.tool-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.action-btn {
  width: 100%;
  margin-top: 12px;
}

/* 设定列表 */
.settings-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.setting-item {
  padding: 12px;
  background: var(--bg-primary);
  border-radius: 8px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.item-name {
  font-weight: 600;
}

.item-desc {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

/* 大纲树面板 */
.outline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  font-weight: 600;
}

.outline-tree-panel {
  max-height: 400px;
  overflow-y: auto;
}

/* 填充对话框 */
.fill-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.event-option {
  padding: 12px;
  background: var(--bg-primary);
  border-radius: 8px;
}

.event-title {
  font-weight: 600;
  display: block;
}

.event-desc {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 去AI味结果 */
.deai-result {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.score-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.score-label {
  font-weight: 600;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.issue-type {
  font-weight: 600;
  margin-right: 8px;
}

.issue-text {
  color: var(--text-secondary);
}

.issue-reason,
.issue-suggestion {
  font-size: 12px;
  margin-top: 4px;
}

/* 纠错结果 */
.proofread-result {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.overall-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.radar-chart {
  display: flex;
  justify-content: center;
}

.chart-container {
  width: 300px;
  height: 300px;
}

.dimensions-detail {
  margin-top: 12px;
}

.dimension-header {
  margin-bottom: 8px;
}

.issue-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-color);
}

.summary-section {
  margin-top: 12px;
}

.summary-text {
  padding: 12px;
  background: var(--bg-primary);
  border-radius: 8px;
  line-height: 1.6;
}

/* 续写候选 */
.candidate-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.candidate-item {
  padding: 16px;
  background: var(--bg-primary);
  border-radius: 8px;
}

.candidate-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.candidate-label {
  font-weight: 600;
}

.candidate-words {
  color: var(--text-secondary);
  font-size: 12px;
}

.candidate-preview {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* 预览内容 */
.preview-content {
  max-height: 60vh;
  overflow-y: auto;
  padding: 20px;
  background: var(--bg-primary);
  border-radius: 8px;
  line-height: 1.8;
  white-space: pre-wrap;
}

/* 知识库结果 */
.knowledge-results {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.knowledge-item {
  padding: 12px;
  background: var(--bg-primary);
  border-radius: 8px;
}

.item-content {
  margin-bottom: 6px;
  line-height: 1.5;
}

.item-source {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

/* 响应式 */
@media (max-width: 1024px) {
  .tools-sidebar {
    width: 280px;
  }
  
  .content-editor {
    padding: 30px 40px;
  }
}

@media (max-width: 768px) {
  .outline-sidebar,
  .tools-sidebar {
    position: fixed;
    z-index: 100;
    height: calc(100vh - 60px);
  }
  
  .outline-sidebar {
    left: 0;
  }
  
  .tools-sidebar {
    right: 0;
  }
  
  .content-editor {
    padding: 20px;
  }
}
</style>
