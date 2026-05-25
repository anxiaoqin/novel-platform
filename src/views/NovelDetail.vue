<template>
  <div class="novel-detail">
    <!-- 顶部导航 -->
    <div class="page-header">
      <el-button @click="goBack" size="small">← 返回</el-button>
      <h2>{{ novel.title || '加载中...' }}</h2>
      <el-button type="primary" @click="showAddChapter = true" size="small">+ 新章节</el-button>
    </div>

    <!-- 小说信息卡片 -->
    <el-card class="info-card">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="字数">{{ wordCount }} 字</el-descriptions-item>
        <el-descriptions-item label="章节数">{{ chapters.length }} 章</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="novel.status === 'completed' ? 'success' : 'primary'">
            {{ novel.status === 'completed' ? '已完成' : '创作中' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="简介" :span="3">{{ novel.description || '暂无简介' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 章节列表 -->
    <el-card class="chapters-card">
      <template #header>
        <span>章节列表</span>
      </template>
      <el-empty v-if="chapters.length === 0" description="暂无章节，点击右上角添加" />
      <el-table v-else :data="chapters" stripe style="width: 100%">
        <el-table-column prop="order" label="序号" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column label="字数" width="100">
          <template #default="{ row }">
            {{ row.content ? row.content.replace(/<[^>]*>/g, '').length : 0 }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="editChapter(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteChapter(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑章节对话框 -->
    <el-dialog 
      v-model="showAddChapter" 
      :title="editingChapter ? '编辑章节' : '添加章节'"
      width="80%"
      top="5vh"
      destroy-on-close
    >
      <div class="chapter-editor">
        <el-input v-model="chapterTitle" placeholder="章节标题" class="chapter-title-input" size="large" />
        
        <!-- 编辑器工具栏 -->
        <div class="editor-toolbar">
          <el-button-group>
            <el-button size="small" @click="insertFormat('bold')" title="加粗"><strong>B</strong></el-button>
            <el-button size="small" @click="insertFormat('italic')" title="斜体"><em>I</em></el-button>
            <el-button size="small" @click="insertFormat('heading')" title="标题">H</el-button>
            <el-button size="small" @click="insertFormat('quote')" title="引用">""</el-button>
          </el-button-group>
          <span class="word-count-inline">字数：{{ contentWordCount }}</span>
        </div>

        <!-- 内容编辑区 -->
        <el-input
          v-model="chapterContent"
          type="textarea"
          :rows="18"
          placeholder="开始创作你的章节内容...&#10;&#10;支持简单格式：&#10;**加粗** _斜体_ ## 标题 > 引用"
          class="chapter-textarea"
        />

        <div class="editor-footer">
          <div></div>
          <div class="action-buttons">
            <el-button @click="showAddChapter = false">取消</el-button>
            <el-button type="primary" @click="saveChapter" :loading="saving">
              {{ editingChapter ? '保存' : '创建' }}
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'

const route = useRoute()
const router = useRouter()

// 数据
const novel = ref({})
const chapters = ref([])
const showAddChapter = ref(false)
const editingChapter = ref(null)
const chapterTitle = ref('')
const chapterContent = ref('')
const saving = ref(false)

// 计算属性
const wordCount = computed(() => {
  return chapters.value.reduce((sum, ch) => {
    const text = ch.content ? ch.content.replace(/<[^>]*>/g, '') : ''
    return sum + text.length
  }, 0)
})

const contentWordCount = computed(() => {
  return chapterContent.value.replace(/\s/g, '').length
})

// 加载数据
const loadNovel = async () => {
  try {
    novel.value = await api.get(`/novels/${route.params.id}`)
  } catch (err) {
    console.error(err)
    ElMessage.error('加载小说失败')
  }
}

const loadChapters = async () => {
  try {
    chapters.value = await api.get(`/novels/${route.params.id}/chapters`)
  } catch (err) {
    console.error('加载章节失败', err)
    chapters.value = []
  }
}

// 简单格式插入
const insertFormat = (type) => {
  const textarea = document.querySelector('.chapter-textarea textarea')
  if (!textarea) return
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const text = chapterContent.value
  const selected = text.substring(start, end)
  
  let before = '', after = ''
  switch (type) {
    case 'bold': before = '**'; after = '**'; break
    case 'italic': before = '_'; after = '_'; break
    case 'heading': before = '## '; after = ''; break
    case 'quote': before = '> '; after = ''; break
  }
  
  chapterContent.value = text.substring(0, start) + before + selected + after + text.substring(end)
}

// 编辑章节
const editChapter = (chapter) => {
  editingChapter.value = chapter
  chapterTitle.value = chapter.title
  chapterContent.value = chapter.content || ''
  showAddChapter.value = true
}

// 保存章节
const saveChapter = async () => {
  if (!chapterTitle.value.trim()) {
    ElMessage.warning('请输入章节标题')
    return
  }

  saving.value = true
  try {
    const data = {
      title: chapterTitle.value,
      content: chapterContent.value
    }

    if (editingChapter.value) {
      await api.put(`/chapters/${editingChapter.value.id}`, data)
      ElMessage.success('章节保存成功')
    } else {
      await api.post(`/novels/${route.params.id}/chapters`, data)
      ElMessage.success('章节创建成功')
    }

    showAddChapter.value = false
    editingChapter.value = null
    chapterTitle.value = ''
    chapterContent.value = ''
    loadChapters()
  } catch (err) {
    console.error(err)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 删除章节
const deleteChapter = async (chapter) => {
  try {
    await ElMessageBox.confirm(`确定删除章节"${chapter.title}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await api.delete(`/chapters/${chapter.id}`)
    ElMessage.success('删除成功')
    loadChapters()
  } catch (err) {
    if (err !== 'cancel') {
      console.error(err)
      ElMessage.error('删除失败')
    }
  }
}

const goBack = () => router.push('/home/novels')

onMounted(() => {
  loadNovel()
  loadChapters()
})
</script>

<style scoped>
.novel-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.page-header h2 {
  flex: 1;
  margin: 0;
}

.info-card {
  margin-bottom: 20px;
}

.chapters-card {
  margin-bottom: 20px;
}

.chapter-editor {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chapter-title-input {
  font-size: 18px;
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.word-count-inline {
  color: #909399;
  font-size: 13px;
}

.chapter-textarea :deep(textarea) {
  font-size: 15px;
  line-height: 1.8;
  font-family: 'Microsoft YaHei', sans-serif;
}

.editor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #e6e6e6;
}

.action-buttons {
  display: flex;
  gap: 10px;
}
</style>
