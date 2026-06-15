<template>
  <div class="timeline-page">
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
        @click="openCreateDialog"
        :disabled="!currentNovelId"
      >
        <el-icon><Plus /></el-icon>
        添加事件
      </el-button>
    </div>

    <!-- 时间线内容 -->
    <div class="timeline-container" v-if="currentNovelId">
      <div class="timeline-wrapper">
        <el-timeline v-if="timelines.length">
          <el-timeline-item
            v-for="(item, index) in sortedTimelines"
            :key="item.id"
            :timestamp="formatTime(item)"
            placement="top"
            :hollow="item.completed"
          >
            <el-card class="timeline-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <div class="card-title">
                    <span class="title">{{ item.title }}</span>
                    <el-tag v-if="item.type" :type="getTypeColor(item.type)" size="small">
                      {{ getTypeLabel(item.type) }}
                    </el-tag>
                  </div>
                  <div class="card-actions">
                    <el-button type="primary" link size="small" @click="openEditDialog(item)">
                      编辑
                    </el-button>
                    <el-button type="danger" link size="small" @click="handleDelete(item)">
                      删除
                    </el-button>
                  </div>
                </div>
              </template>
              <div class="card-body">
                <p class="description">{{ item.description || '暂无描述' }}</p>
                
                <!-- 涉及角色 -->
                <div class="characters-section" v-if="item.characters?.length">
                  <span class="section-label">涉及角色：</span>
                  <el-tag
                    v-for="char in item.characters"
                    :key="char.id || char"
                    size="small"
                    class="char-tag"
                  >
                    {{ typeof char === 'object' ? char.name : char }}
                  </el-tag>
                </div>
                
                <!-- 相关章节 -->
                <div class="chapters-section" v-if="item.chapter_id || item.related_chapters?.length">
                  <span class="section-label">相关章节：</span>
                  <el-link 
                    v-if="item.chapter_id" 
                    type="primary" 
                    :underline="false"
                    @click="goToChapter(item.chapter_id)"
                  >
                    第{{ item.chapter_id }}章
                  </el-link>
                  <el-link 
                    v-for="ch in item.related_chapters"
                    :key="ch"
                    type="primary" 
                    :underline="false"
                    @click="goToChapter(ch)"
                  >
                    第{{ ch }}章
                  </el-link>
                </div>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
        
        <el-empty v-else-if="!loading" description="暂无时间线事件，点击上方按钮添加">
          <el-button type="primary" @click="openCreateDialog">添加第一个事件</el-button>
        </el-empty>
      </div>

      <div class="loading-container" v-if="loading">
        <el-skeleton :rows="5" animated />
      </div>
    </div>

    <el-empty v-else description="请先选择作品" />

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑事件' : '添加事件'"
      width="600px"
      @close="resetForm"
    >
      <el-form 
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="90px"
      >
        <el-form-item label="事件标题" prop="title">
          <el-input 
            v-model="formData.title" 
            placeholder="请输入事件标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始时间" prop="start_time">
              <el-date-picker
                v-model="formData.start_time"
                type="datetime"
                placeholder="选择开始时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间" prop="end_time">
              <el-date-picker
                v-model="formData.end_time"
                type="datetime"
                placeholder="选择结束时间（可选）"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="事件类型" prop="type">
          <el-select v-model="formData.type" placeholder="选择类型">
            <el-option label="主线事件" value="main" />
            <el-option label="支线事件" value="sub" />
            <el-option label="回忆" value="flashback" />
            <el-option label="未来" value="future" />
            <el-option label="日常" value="daily" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="事件描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="详细描述这个事件..."
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="涉及角色">
          <el-select
            v-model="formData.characters"
            multiple
            placeholder="选择涉及的角色"
            style="width: 100%"
          >
            <el-option
              v-for="char in availableCharacters"
              :key="char.id"
              :label="char.name"
              :value="char.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="相关章节">
          <el-input
            v-model="relatedChaptersStr"
            placeholder="输入相关章节ID，多个用逗号分隔"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存' : '添加' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { 
  getTimelines, 
  createTimeline, 
  updateTimeline, 
  deleteTimeline 
} from '@/api/modules/timeline'
import { getNovels } from '@/api/modules/novel'
import { getCharacters } from '@/api/modules/character'

const router = useRouter()

// 状态
const novels = ref([])
const currentNovelId = ref(null)
const timelines = ref([])
const availableCharacters = ref([])
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)
const formRef = ref(null)
const relatedChaptersStr = ref('')

// 时间线类型配置
const typeMap = {
  main: { label: '主线', color: 'danger' },
  sub: { label: '支线', color: 'warning' },
  flashback: { label: '回忆', color: 'info' },
  future: { label: '未来', color: '' },
  daily: { label: '日常', color: 'success' }
}

// 排序后的时间线
const sortedTimelines = computed(() => {
  return [...timelines.value].sort((a, b) => {
    const timeA = a.start_time ? new Date(a.start_time) : new Date(0)
    const timeB = b.start_time ? new Date(b.start_time) : new Date(0)
    return timeA - timeB
  })
})

// 表单数据
const formData = reactive({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  type: 'main',
  characters: [],
  chapter_id: null
})

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: '请输入事件标题', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择事件类型', trigger: 'change' }
  ]
}

// 获取作品列表
const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.data || []
    if (novels.value.length && !currentNovelId.value) {
      currentNovelId.value = novels.value[0].id
      loadTimelines()
      loadCharacters()
    }
  } catch (err) {
    console.error('加载作品列表失败:', err)
  }
}

// 加载时间线
const loadTimelines = async () => {
  if (!currentNovelId.value) return
  loading.value = true
  try {
    const res = await getTimelines(currentNovelId.value)
    timelines.value = res.data || []
  } catch (err) {
    console.error('加载时间线失败:', err)
    ElMessage.error('加载时间线失败')
  } finally {
    loading.value = false
  }
}

// 加载角色列表
const loadCharacters = async () => {
  if (!currentNovelId.value) return
  try {
    const res = await getCharacters(currentNovelId.value)
    availableCharacters.value = res.data || []
  } catch (err) {
    console.error('加载角色列表失败:', err)
  }
}

// 作品切换
const handleNovelChange = () => {
  loadTimelines()
  loadCharacters()
}

// 格式化时间
const formatTime = (item) => {
  if (!item.start_time) return '时间未知'
  const date = new Date(item.start_time)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取类型标签
const getTypeLabel = (type) => {
  return typeMap[type]?.label || type
}

// 获取类型颜色
const getTypeColor = (type) => {
  return typeMap[type]?.color || ''
}

// 打开创建对话框
const openCreateDialog = () => {
  isEdit.value = false
  editingId.value = null
  relatedChaptersStr.value = ''
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (item) => {
  isEdit.value = true
  editingId.value = item.id
  formData.title = item.title
  formData.description = item.description || ''
  formData.start_time = item.start_time || ''
  formData.end_time = item.end_time || ''
  formData.type = item.type || 'main'
  formData.characters = item.characters?.map(c => c.id || c) || []
  formData.chapter_id = item.chapter_id || null
  
  // 处理相关章节
  if (item.related_chapters?.length) {
    relatedChaptersStr.value = item.related_chapters.join(', ')
  } else if (item.chapter_id) {
    relatedChaptersStr.value = String(item.chapter_id)
  } else {
    relatedChaptersStr.value = ''
  }
  
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  formData.title = ''
  formData.description = ''
  formData.start_time = ''
  formData.end_time = ''
  formData.type = 'main'
  formData.characters = []
  formData.chapter_id = null
  relatedChaptersStr.value = ''
  formRef.value?.resetFields()
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    const payload = {
      title: formData.title,
      description: formData.description,
      start_time: formData.start_time,
      end_time: formData.end_time || undefined,
      type: formData.type,
      characters: formData.characters
    }
    
    // 处理相关章节
    if (relatedChaptersStr.value) {
      const chapters = relatedChaptersStr.value
        .split(/[,，]/)
        .map(s => parseInt(s.trim()))
        .filter(n => !isNaN(n))
      if (chapters.length > 0) {
        payload.chapter_id = chapters[0]
        payload.related_chapters = chapters
      }
    }
    
    if (isEdit.value) {
      await updateTimeline(currentNovelId.value, editingId.value, payload)
      ElMessage.success('更新成功')
    } else {
      await createTimeline(currentNovelId.value, payload)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadTimelines()
  } catch (err) {
    console.error('保存失败:', err)
    ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
  } finally {
    submitting.value = false
  }
}

// 删除事件
const handleDelete = async (item) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除事件「${item.title}」吗？`,
      '删除确认',
      { type: 'warning' }
    )
    await deleteTimeline(currentNovelId.value, item.id)
    ElMessage.success('删除成功')
    loadTimelines()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 跳转到章节
const goToChapter = (chapterId) => {
  router.push(`/home/novels/${currentNovelId.value}?chapter=${chapterId}`)
}

// 初始化
onMounted(() => {
  loadNovels()
})
</script>

<style scoped>
.timeline-page {
  padding: 20px;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.novel-select {
  width: 200px;
}

.timeline-container {
  flex: 1;
  overflow-y: auto;
}

.timeline-wrapper {
  max-width: 900px;
  margin: 0 auto;
}

.timeline-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.timeline-card:hover {
  transform: translateX(4px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-title .title {
  font-size: 16px;
  font-weight: 600;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-body {
  padding: 4px 0;
}

.description {
  color: #555;
  line-height: 1.7;
  margin-bottom: 12px;
}

.characters-section,
.chapters-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.section-label {
  font-size: 12px;
  color: #999;
  flex-shrink: 0;
}

.char-tag {
  margin-right: 4px;
}

.loading-container {
  padding: 40px 20px;
}

/* Element Plus Timeline 样式覆盖 */
:deep(.el-timeline-item__content) {
  padding-bottom: 8px;
}

:deep(.el-timeline-item__timestamp) {
  font-size: 13px;
  color: #666;
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
  
  .timeline-wrapper {
    padding: 0 10px;
  }
}
</style>
