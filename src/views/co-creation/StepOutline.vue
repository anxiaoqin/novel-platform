<template>
  <div class="step-outline-container">
    <!-- 顶部工具栏 -->
    <header class="outline-header">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <h2 class="page-title">大纲管理</h2>
      </div>
      <div class="header-center">
        <el-button-group>
          <el-button size="small" :type="activeView === 'tree' ? 'primary' : ''" @click="activeView = 'tree'">
            <el-icon><Operation /></el-icon> 树形视图
          </el-button>
          <el-button size="small" :type="activeView === 'timeline' ? 'primary' : ''" @click="activeView = 'timeline'">
            <el-icon><Time /></el-icon> 时间线
          </el-button>
          <el-button size="small" :type="activeView === 'table' ? 'primary' : ''" @click="activeView = 'table'">
            <el-icon><List /></el-icon> 表格视图
          </el-button>
        </el-button-group>
      </div>
      <div class="header-right">
        <el-button size="small" @click="openVersionDialog">
          <el-icon><FolderOpened /></el-icon> 版本
        </el-button>
        <el-button size="small" @click="saveOutline">
          <el-icon><Check /></el-icon> 保存
        </el-button>
        <el-button type="primary" size="small" @click="openAIAssist">
          <el-icon><MagicStick /></el-icon> AI辅助
        </el-button>
      </div>
    </header>

    <!-- 主体内容 -->
    <div class="outline-main">
      <!-- 左侧层级面板 -->
      <aside class="level-panel">
        <div class="panel-header">
          <span>层级结构</span>
          <el-button text size="small" @click="addLevel">
            <el-icon><Plus /></el-icon>
          </el-button>
        </div>
        <div class="level-list">
          <div
            v-for="level in levelConfig"
            :key="level.key"
            class="level-item"
            :class="{ active: currentLevel === level.key }"
            @click="currentLevel = level.key"
          >
            <span class="level-icon">{{ level.icon }}</span>
            <span class="level-name">{{ level.name }}</span>
            <span class="level-count">{{ getLevelCount(level.key) }}</span>
          </div>
        </div>
      </aside>

      <!-- 中间大纲区域 -->
      <main class="outline-content">
        <!-- 工具栏 -->
        <div class="content-toolbar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索大纲..."
            size="small"
            clearable
            style="width: 200px;"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <div class="toolbar-actions">
            <el-button size="small" @click="addNode">
              <el-icon><Plus /></el-icon> 新增
            </el-button>
            <el-button size="small" :disabled="!selectedNode" @click="editNode">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button size="small" :disabled="!selectedNode" @click="deleteNode">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
            <el-button size="small" :disabled="!selectedNode" @click="generateContent">
              <el-icon><EditPen /></el-icon> 生成内容
            </el-button>
          </div>
        </div>

        <!-- 树形视图 -->
        <div class="tree-view" v-show="activeView === 'tree'">
          <el-tree
            ref="treeRef"
            :data="filteredOutline"
            :props="treeProps"
            node-key="id"
            default-expand-all
            highlight-current
            :expand-on-click-node="false"
            :filter-node-method="filterNode"
            @node-click="handleNodeClick"
            @node-drop="handleNodeDrop"
            draggable
          >
            <template #default="{ node, data }">
              <div class="tree-node-content" @mouseenter="hoverNodeId = data.id" @mouseleave="hoverNodeId = null">
                <span class="node-level-icon">{{ getLevelIcon(data.level) }}</span>
                <span class="node-title">{{ node.label }}</span>
                <span class="node-meta" v-if="data.word_count">
                  {{ data.word_count }}字
                </span>
                <span class="node-source" v-if="data.source === 'ai_suggested'">
                  <el-tag size="small" type="info">AI建议</el-tag>
                </span>
                
                <div class="node-actions" v-if="hoverNodeId === data.id">
                  <el-button text size="small" @click.stop="addChildNode(data)">
                    <el-icon><Plus /></el-icon>
                  </el-button>
                  <el-button text size="small" @click.stop="toggleNodeStatus(data)">
                    <el-icon v-if="data.status === 'completed'"><CircleCheckFilled /></el-icon>
                    <el-icon v-else><CircleCheck /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
          </el-tree>
          
          <el-empty v-if="!filteredOutline.length" description="暂无大纲，点击上方新增按钮创建" />
        </div>

        <!-- 时间线视图 -->
        <div class="timeline-view" v-show="activeView === 'timeline'">
          <div class="timeline-container">
            <div class="timeline-line"></div>
            <div
              v-for="(event, idx) in timelineItems"
              :key="event.id"
              class="timeline-item"
              :class="{ left: idx % 2 === 0, right: idx % 2 !== 0 }"
            >
              <div class="timeline-marker">
                <span class="marker-dot"></span>
                <span class="marker-time">{{ event.time || `第${idx + 1}幕` }}</span>
              </div>
              <div class="timeline-content" @click="handleTimelineClick(event)">
                <div class="content-header">
                  <span class="content-title">{{ event.title }}</span>
                  <el-tag size="small" :type="getTypeColor(event.type)">{{ event.type }}</el-tag>
                </div>
                <div class="content-desc">{{ event.description }}</div>
                <div class="content-participants" v-if="event.participants?.length">
                  <el-tag
                    v-for="p in event.participants"
                    :key="p"
                    size="small"
                  >
                    {{ p }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 表格视图 -->
        <div class="table-view" v-show="activeView === 'table'">
          <el-table
            :data="tableData"
            border
            stripe
            @row-click="handleRowClick"
          >
            <el-table-column prop="order" label="序号" width="80" />
            <el-table-column prop="level" label="层级" width="100">
              <template #default="{ row }">
                {{ getLevelName(row.level) }}
              </template>
            </el-table-column>
            <el-table-column prop="title" label="标题" min-width="200" />
            <el-table-column prop="type" label="类型" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ row.type || '-' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="participants" label="参与者" width="180">
              <template #default="{ row }">
                <span v-if="row.participants?.length">
                  {{ row.participants.join(', ') }}
                </span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'completed' ? 'success' : 'info'" size="small">
                  {{ row.status === 'completed' ? '已完成' : '进行中' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button text size="small" @click.stop="editNode(row)">编辑</el-button>
                <el-button text size="small" type="danger" @click.stop="deleteNode(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </main>

      <!-- 右侧详情面板 -->
      <aside class="detail-panel" v-if="selectedNode">
        <div class="panel-header">
          <span>节点详情</span>
          <el-button text size="small" @click="selectedNode = null">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
        
        <div class="detail-content">
          <div class="detail-field">
            <label>标题</label>
            <el-input v-model="selectedNode.title" size="small" @change="updateNode" />
          </div>
          
          <div class="detail-field">
            <label>描述</label>
            <el-input
              v-model="selectedNode.description"
              type="textarea"
              :rows="4"
              placeholder="输入事件描述..."
              @change="updateNode"
            />
          </div>
          
          <div class="detail-field">
            <label>类型</label>
            <el-select v-model="selectedNode.type" size="small" placeholder="选择类型" @change="updateNode">
              <el-option label="铺垫" value="铺垫" />
              <el-option label="冲突" value="冲突" />
              <el-option label="反转" value="反转" />
              <el-option label="高潮" value="高潮" />
              <el-option label="过渡" value="过渡" />
              <el-option label="收尾" value="收尾" />
            </el-select>
          </div>
          
          <div class="detail-field">
            <label>参与者</label>
            <el-select
              v-model="selectedNode.participants"
              multiple
              size="small"
              placeholder="选择角色"
              @change="updateNode"
            >
              <el-option
                v-for="char in characters"
                :key="char.id"
                :label="char.name"
                :value="char.name"
              />
            </el-select>
          </div>
          
          <div class="detail-field">
            <label>状态</label>
            <el-radio-group v-model="selectedNode.status" size="small" @change="updateNode">
              <el-radio-button label="in_progress">进行中</el-radio-button>
              <el-radio-button label="completed">已完成</el-radio-button>
            </el-radio-group>
          </div>
          
          <div class="detail-field">
            <label>字数</label>
            <el-input-number v-model="selectedNode.word_count" :min="0" size="small" @change="updateNode" />
          </div>
          
          <div class="detail-actions">
            <el-button type="primary" size="small" @click="generateForNode">
              <el-icon><EditPen /></el-icon> 生成内容
            </el-button>
            <el-button size="small" @click="copyNode">
              <el-icon><CopyDocument /></el-icon> 复制
            </el-button>
          </div>
        </div>
      </aside>
    </div>

    <!-- 新增/编辑节点对话框 -->
    <el-dialog
      v-model="nodeDialogVisible"
      :title="editingNode?.id ? '编辑节点' : '新增节点'"
      width="600px"
    >
      <el-form :model="nodeForm" label-width="80px">
        <el-form-item label="层级">
          <el-select v-model="nodeForm.level" size="small">
            <el-option
              v-for="level in levelConfig"
              :key="level.key"
              :label="level.name"
              :value="level.key"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="标题">
          <el-input v-model="nodeForm.title" size="small" placeholder="输入节点标题" />
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input
            v-model="nodeForm.description"
            type="textarea"
            :rows="4"
            placeholder="输入事件描述..."
          />
        </el-form-item>
        
        <el-form-item label="类型">
          <el-select v-model="nodeForm.type" size="small" placeholder="选择类型">
            <el-option label="铺垫" value="铺垫" />
            <el-option label="冲突" value="冲突" />
            <el-option label="反转" value="反转" />
            <el-option label="高潮" value="高潮" />
            <el-option label="过渡" value="过渡" />
            <el-option label="收尾" value="收尾" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="参与者">
          <el-select v-model="nodeForm.participants" multiple size="small" placeholder="选择角色">
            <el-option
              v-for="char in characters"
              :key="char.id"
              :label="char.name"
              :value="char.name"
            />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="nodeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveNode">确定</el-button>
      </template>
    </el-dialog>

    <!-- 版本管理对话框 -->
    <el-dialog v-model="versionDialogVisible" title="版本管理" width="700px">
      <div class="version-header">
        <el-button type="primary" size="small" @click="saveVersion">
          <el-icon><Plus /></el-icon> 保存当前版本
        </el-button>
      </div>
      
      <div class="version-list">
        <div
          v-for="version in versionList"
          :key="version.id"
          class="version-item"
          :class="{ active: version.is_active }"
        >
          <div class="version-info">
            <div class="version-name">
              {{ version.version_name }}
              <el-tag v-if="version.is_active" size="small" type="success">当前</el-tag>
            </div>
            <div class="version-meta">
              <span>{{ formatTime(version.created_at) }}</span>
              <span>{{ version.node_count || 0 }} 个节点</span>
            </div>
          </div>
          <div class="version-actions">
            <el-button size="small" @click="previewVersion(version)" :disabled="version.is_active">
              预览
            </el-button>
            <el-button size="small" @click="activateVersion(version)" :disabled="version.is_active">
              激活
            </el-button>
            <el-button size="small" type="danger" @click="deleteVersion(version)" :disabled="version.is_active">
              删除
            </el-button>
          </div>
        </div>
        
        <el-empty v-if="!versionList.length" description="暂无版本记录" />
      </div>
    </el-dialog>

    <!-- AI辅助对话框 -->
    <el-dialog v-model="aiAssistDialogVisible" title="AI大纲辅助" width="700px">
      <div class="ai-assist-content">
        <div class="assist-section">
          <div class="section-title">智能生成</div>
          <el-input
            v-model="aiPrompt"
            type="textarea"
            :rows="3"
            placeholder="描述你想要的剧情走向，AI将帮你生成大纲..."
          />
          <div class="assist-actions">
            <el-button type="primary" :loading="generating" @click="generateOutline">
              <el-icon><MagicStick /></el-icon> 生成大纲
            </el-button>
            <el-button :loading="generating" @click="generateOutlineStream">
              <el-icon><VideoPlay /></el-icon> 流式生成
            </el-button>
          </div>
        </div>
        
        <div class="assist-section">
          <div class="section-title">批量操作</div>
          <div class="batch-actions">
            <el-button size="small" @click="batchComplete">标记全部完成</el-button>
            <el-button size="small" @click="batchAssignType">批量设置类型</el-button>
            <el-button size="small" type="danger" @click="batchDelete">批量删除</el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft, Operation, Time, List, FolderOpened, Check, MagicStick,
  Plus, Search, Edit, Delete, EditPen, Close, CircleCheck, CircleCheckFilled,
  CopyDocument, VideoPlay
} from '@element-plus/icons-vue'
import { createSSEStream, extractContent } from '@/api/sse'
import api from '@/api'

// 路由
const router = useRouter()
const route = useRoute()

// 状态
const novelId = ref(route.query.novel_id || 1)
const chapterId = ref(route.query.chapter_id || 1)
const activeView = ref('tree')
const searchKeyword = ref('')
const currentLevel = ref('chapter')

// 层级配置
const levelConfig = [
  { key: 'volume', name: '卷', icon: '📚' },
  { key: 'chapter', name: '章', icon: '📖' },
  { key: 'scene', name: '场景', icon: '🎬' },
  { key: 'paragraph', name: '段落', icon: '📝' }
]

// 树形相关
const treeRef = ref(null)
const treeProps = {
  label: 'title',
  children: 'children'
}
const outlineData = ref([])
const hoverNodeId = ref(null)
const selectedNode = ref(null)

// 时间线
const timelineItems = computed(() => {
  return flattenOutline(outlineData.value)
})

// 表格数据
const tableData = computed(() => {
  return flattenOutline(outlineData.value).map((item, idx) => ({
    ...item,
    order: idx + 1
  }))
})

// 过滤后的大纲
const filteredOutline = computed(() => {
  if (!searchKeyword.value) return outlineData.value
  return outlineData.value // 实际过滤由 el-tree 的 filter-node-method 处理
})

// 角色列表
const characters = ref([])

// 对话框
const nodeDialogVisible = ref(false)
const editingNode = ref(null)
const nodeForm = reactive({
  level: 'scene',
  title: '',
  description: '',
  type: '',
  participants: []
})

const versionDialogVisible = ref(false)
const versionList = ref([])

const aiAssistDialogVisible = ref(false)
const aiPrompt = ref('')
const generating = ref(false)

// 流式生成控制器
const streamController = ref(null)

// 监听搜索
watch(searchKeyword, (val) => {
  treeRef.value?.filter(val)
})

// 生命周期
onMounted(() => {
  loadOutline()
  loadCharacters()
  loadVersions()
})

onUnmounted(() => {
  if (streamController.value) {
    streamController.value.abort()
  }
})

// 加载大纲
async function loadOutline() {
  try {
    const res = await api.get(`/novels/${novelId.value}/outline-tree`)
    if (res.data.success) {
      outlineData.value = res.data.data.outline || []
    }
  } catch (err) {
    console.error('加载大纲失败', err)
    // 使用示例数据
    outlineData.value = [
      {
        id: 1,
        title: '第一卷 觉醒',
        level: 'volume',
        children: [
          {
            id: 2,
            title: '第一章 离开宗门',
            level: 'chapter',
            children: [
              {
                id: 3,
                title: '场景1：悬崖思考',
                level: 'scene',
                description: '林风独自站在悬崖边思考人生',
                type: '铺垫'
              },
              {
                id: 4,
                title: '场景2：遭遇妖兽',
                level: 'scene',
                description: '危机降临，林风被迫战斗',
                type: '冲突'
              }
            ]
          }
        ]
      }
    ]
  }
}

// 加载角色
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

// 加载版本
async function loadVersions() {
  try {
    const res = await api.get(`/novels/${novelId.value}/outline-versions`)
    if (res.data.success) {
      versionList.value = res.data.data || []
    }
  } catch (err) {
    console.error('加载版本失败', err)
    versionList.value = []
  }
}

// 保存大纲
async function saveOutline() {
  try {
    await api.post('/ai/save-outline-events', {
      novel_id: novelId.value,
      chapter_id: chapterId.value,
      events: flattenOutline(outlineData.value).map(item => ({
        id: item.id,
        title: item.title,
        description: item.description,
        level: item.level,
        type: item.type,
        participants: item.participants,
        status: item.status,
        parent_id: item.parent_id
      }))
    })
    ElMessage.success('大纲保存成功')
  } catch (err) {
    ElMessage.error('保存失败')
  }
}

// 保存版本
async function saveVersion() {
  try {
    const { value: versionName } = await ElMessageBox.prompt('请输入版本名称', '保存版本', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    await api.post(`/novels/${novelId.value}/outline-versions`, {
      version_name: versionName
    })
    
    ElMessage.success('版本保存成功')
    loadVersions()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('保存失败')
  }
}

// 激活版本
async function activateVersion(version) {
  try {
    await ElMessageBox.confirm('激活此版本将覆盖当前大纲，是否继续？', '激活版本', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    await api.put(`/novels/${novelId.value}/outline-versions/${version.id}/activate`)
    ElMessage.success('版本激活成功')
    loadOutline()
    loadVersions()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('激活失败')
  }
}

// 删除版本
async function deleteVersion(version) {
  try {
    await ElMessageBox.confirm('确定删除此版本？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    await api.delete(`/novels/${novelId.value}/outline-versions/${version.id}`)
    ElMessage.success('删除成功')
    loadVersions()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('删除失败')
  }
}

// 预览版本
function previewVersion(version) {
  ElMessage.info('预览功能开发中')
}

// 工具函数
function flattenOutline(nodes, parentId = null) {
  const result = []
  for (const node of nodes) {
    result.push({ ...node, parent_id: parentId })
    if (node.children?.length) {
      result.push(...flattenOutline(node.children, node.id))
    }
  }
  return result
}

function getLevelCount(level) {
  return flattenOutline(outlineData.value).filter(n => n.level === level).length
}

function getLevelIcon(level) {
  const icons = { volume: '📚', chapter: '📖', scene: '🎬', paragraph: '📝' }
  return icons[level] || '📄'
}

function getLevelName(level) {
  const names = { volume: '卷', chapter: '章', scene: '场景', paragraph: '段落' }
  return names[level] || level
}

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

function formatTime(time) {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

// 树操作
function filterNode(value, data) {
  if (!searchKeyword.value) return true
  return data.title?.includes(searchKeyword.value) || data.description?.includes(searchKeyword.value)
}

function handleNodeClick(data) {
  selectedNode.value = { ...data }
}

function handleRowClick(row) {
  selectedNode.value = { ...row }
}

function handleTimelineClick(event) {
  selectedNode.value = { ...event }
}

// 节点拖拽
async function handleNodeDrop(draggingNode, dropNode, dropType) {
  await saveOutline()
}

// 新增节点
function addNode() {
  editingNode.value = null
  Object.assign(nodeForm, {
    level: currentLevel.value,
    title: '',
    description: '',
    type: '',
    participants: []
  })
  nodeDialogVisible.value = true
}

// 新增子节点
function addChildNode(parent) {
  editingNode.value = null
  Object.assign(nodeForm, {
    level: getChildLevel(parent.level),
    title: '',
    description: '',
    type: '',
    participants: parent.participants || []
  })
  nodeDialogVisible.value = true
}

function getChildLevel(level) {
  const levels = ['volume', 'chapter', 'scene', 'paragraph']
  const idx = levels.indexOf(level)
  return idx < levels.length - 1 ? levels[idx + 1] : level
}

// 编辑节点
function editNode(node) {
  editingNode.value = node || selectedNode.value
  Object.assign(nodeForm, {
    level: editingNode.value.level,
    title: editingNode.value.title,
    description: editingNode.value.description,
    type: editingNode.value.type || '',
    participants: editingNode.value.participants || []
  })
  nodeDialogVisible.value = true
}

// 保存节点
function saveNode() {
  if (!nodeForm.title) {
    ElMessage.warning('请输入标题')
    return
  }
  
  if (editingNode.value?.id) {
    // 更新
    updateNodeInTree(outlineData.value, editingNode.value.id, {
      title: nodeForm.title,
      description: nodeForm.description,
      type: nodeForm.type,
      participants: nodeForm.participants
    })
    if (selectedNode.value?.id === editingNode.value.id) {
      Object.assign(selectedNode.value, nodeForm)
    }
  } else {
    // 新增
    const newNode = {
      id: Date.now(),
      title: nodeForm.title,
      description: nodeForm.description,
      type: nodeForm.type,
      participants: nodeForm.participants,
      level: nodeForm.level,
      source: 'user_created',
      status: 'in_progress',
      children: []
    }
    
    if (selectedNode.value && ['volume', 'chapter', 'scene'].includes(selectedNode.value.level)) {
      if (!selectedNode.value.children) selectedNode.value.children = []
      selectedNode.value.children.push(newNode)
    } else {
      outlineData.value.push(newNode)
    }
  }
  
  nodeDialogVisible.value = false
  saveOutline()
}

function updateNodeInTree(nodes, id, updates) {
  for (const node of nodes) {
    if (node.id === id) {
      Object.assign(node, updates)
      return true
    }
    if (node.children && updateNodeInTree(node.children, id, updates)) {
      return true
    }
  }
  return false
}

// 删除节点
async function deleteNode(node) {
  const target = node || selectedNode.value
  if (!target) return
  
  try {
    await ElMessageBox.confirm('确定删除此节点及其子节点？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    removeNodeFromTree(outlineData.value, target.id)
    if (selectedNode.value?.id === target.id) {
      selectedNode.value = null
    }
    ElMessage.success('删除成功')
    saveOutline()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('删除失败')
  }
}

function removeNodeFromTree(nodes, id) {
  const idx = nodes.findIndex(n => n.id === id)
  if (idx > -1) {
    nodes.splice(idx, 1)
    return true
  }
  for (const node of nodes) {
    if (node.children && removeNodeFromTree(node.children, id)) {
      return true
    }
  }
  return false
}

// 更新节点
function updateNode() {
  // 已在 selectedNode 中更新，保存
  updateNodeInTree(outlineData.value, selectedNode.value.id, selectedNode.value)
  saveOutline()
}

// 切换节点状态
function toggleNodeStatus(node) {
  node.status = node.status === 'completed' ? 'in_progress' : 'completed'
  updateNodeInTree(outlineData.value, node.id, { status: node.status })
  saveOutline()
}

// 复制节点
function copyNode() {
  if (!selectedNode.value) return
  const copy = { ...selectedNode.value, id: Date.now(), title: selectedNode.value.title + '(副本)' }
  outlineData.value.push(copy)
  ElMessage.success('已复制')
  saveOutline()
}

// 为节点生成内容
function generateForNode() {
  if (!selectedNode.value) return
  router.push({
    path: '/co-creation/step-fill',
    query: {
      novel_id: novelId.value,
      chapter_id: chapterId.value,
      event_id: selectedNode.value.id
    }
  })
}

// 生成内容
function generateContent() {
  generateForNode()
}

// 添加层级
function addLevel() {
  ElMessage.info('层级结构由系统预设')
}

// 节点点击
function handleNodeClick(data) {
  selectedNode.value = { ...data }
}

// AI辅助
function openAIAssist() {
  aiAssistDialogVisible.value = true
}

// 生成大纲（非流式）
async function generateOutline() {
  if (!aiPrompt.value.trim()) {
    ElMessage.warning('请输入大纲描述')
    return
  }
  
  generating.value = true
  try {
    const res = await api.post('/ai/create-outline', {
      novel_id: novelId.value,
      description: aiPrompt.value
    })
    
    if (res.data.success) {
      outlineData.value = res.data.data.outline || []
      ElMessage.success('大纲生成成功')
      aiAssistDialogVisible.value = false
    }
  } catch (err) {
    ElMessage.error('生成失败')
  } finally {
    generating.value = false
  }
}

// 流式生成大纲
function generateOutlineStream() {
  if (!aiPrompt.value.trim()) {
    ElMessage.warning('请输入大纲描述')
    return
  }
  
  generating.value = true
  let accumulatedContent = ''
  
  streamController.value = createSSEStream('/ai/create-outline/stream', {
    novel_id: novelId.value,
    description: aiPrompt.value
  }, {
    onMessage: (data) => {
      const content = extractContent(data)
      if (content) {
        accumulatedContent += content
      }
    },
    onDone: () => {
      generating.value = false
      // 尝试解析结果
      try {
        const result = JSON.parse(accumulatedContent)
        outlineData.value = result.outline || []
        ElMessage.success('大纲生成成功')
      } catch (e) {
        ElMessage.error('解析结果失败')
      }
      aiAssistDialogVisible.value = false
    },
    onError: (err) => {
      generating.value = false
      ElMessage.error('生成失败: ' + err.message)
    }
  })
}

// 批量操作
function batchComplete() {
  flattenOutline(outlineData.value).forEach(n => {
    n.status = 'completed'
  })
  ElMessage.success('已标记全部完成')
  saveOutline()
}

function batchAssignType() {
  ElMessageBox.prompt('请输入要设置的类型', '批量设置类型', {
    confirmButtonText: '确定',
    cancelButtonText: '取消'
  }).then(({ value }) => {
    flattenOutline(outlineData.value).forEach(n => {
      n.type = value
    })
    ElMessage.success('已批量设置类型')
    saveOutline()
  }).catch(() => {})
}

function batchDelete() {
  ElMessageBox.confirm('确定删除所有节点？此操作不可恢复！', '危险操作', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    outlineData.value = []
    selectedNode.value = null
    ElMessage.success('已清空大纲')
    saveOutline()
  }).catch(() => {})
}

// 版本管理
function openVersionDialog() {
  loadVersions()
  versionDialogVisible.value = true
}

// 返回
function goBack() {
  router.back()
}
</script>

<style scoped>
.step-outline-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
}

/* 头部 */
.outline-header {
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
.outline-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧面板 */
.level-panel {
  width: 180px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  font-weight: 600;
  border-bottom: 1px solid var(--border-color);
}

.level-list {
  padding: 8px;
}

.level-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.level-item:hover {
  background: var(--bg-primary);
}

.level-item.active {
  background: var(--brand-primary);
  color: white;
}

.level-icon {
  font-size: 16px;
}

.level-name {
  flex: 1;
}

.level-count {
  font-size: 12px;
  color: var(--text-secondary);
}

.level-item.active .level-count {
  color: rgba(255,255,255,0.7);
}

/* 内容区 */
.outline-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.toolbar-actions {
  display: flex;
  gap: 8px;
}

/* 树形视图 */
.tree-view {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.tree-node-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  padding-right: 8px;
}

.node-level-icon {
  font-size: 16px;
}

.node-title {
  flex: 1;
}

.node-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

.node-source {
  margin-left: 8px;
}

.node-actions {
  display: flex;
  gap: 4px;
}

/* 时间线视图 */
.timeline-view {
  flex: 1;
  padding: 40px 20px;
  overflow-y: auto;
}

.timeline-container {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
}

.timeline-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border-color);
  transform: translateX(-50%);
}

.timeline-item {
  display: flex;
  margin-bottom: 30px;
  position: relative;
}

.timeline-item.left {
  flex-direction: row;
  padding-right: calc(50% + 30px);
}

.timeline-item.right {
  flex-direction: row-reverse;
  padding-left: calc(50% + 30px);
}

.timeline-marker {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.marker-dot {
  width: 12px;
  height: 12px;
  background: var(--brand-primary);
  border-radius: 50%;
}

.marker-time {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.timeline-content {
  flex: 1;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.timeline-content:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.content-title {
  font-weight: 600;
}

.content-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.content-participants {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

/* 表格视图 */
.table-view {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

/* 右侧详情面板 */
.detail-panel {
  width: 300px;
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-color);
}

.detail-content {
  padding: 16px;
}

.detail-field {
  margin-bottom: 16px;
}

.detail-field label {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.detail-field :deep(.el-select) {
  width: 100%;
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 20px;
}

/* 版本列表 */
.version-header {
  margin-bottom: 16px;
}

.version-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.version-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--bg-primary);
  border-radius: 8px;
  border: 2px solid transparent;
}

.version-item.active {
  border-color: var(--brand-primary);
}

.version-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  margin-bottom: 4px;
}

.version-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: var(--text-secondary);
}

.version-actions {
  display: flex;
  gap: 8px;
}

/* AI辅助 */
.ai-assist-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.assist-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  font-weight: 600;
}

.assist-actions {
  display: flex;
  gap: 12px;
}

.batch-actions {
  display: flex;
  gap: 8px;
}

/* 响应式 */
@media (max-width: 1024px) {
  .level-panel {
    width: 140px;
  }
  
  .detail-panel {
    width: 260px;
  }
}

@media (max-width: 768px) {
  .level-panel {
    display: none;
  }
  
  .detail-panel {
    position: fixed;
    right: 0;
    top: 60px;
    bottom: 0;
    z-index: 100;
    width: 300px;
    box-shadow: -4px 0 12px rgba(0,0,0,0.1);
  }
}
</style>
