<template>
  <div class="worlds-page">
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
        <el-input
          v-model="searchKeyword"
          placeholder="搜索世界观..."
          class="search-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <el-button 
        type="primary" 
        @click="openCreateDialog"
        :disabled="!currentNovelId"
      >
        <el-icon><Plus /></el-icon>
        新建世界观
      </el-button>
    </div>

    <!-- 世界观卡片网格 -->
    <div class="world-grid" v-if="filteredWorlds.length">
      <el-card 
        v-for="world in filteredWorlds" 
        :key="world.id" 
        class="world-card"
        shadow="hover"
      >
        <template #header>
          <div class="card-header">
            <span class="world-name">{{ world.name }}</span>
            <el-tag :type="getCategoryType(world.category)" size="small">
              {{ getCategoryLabel(world.category) }}
            </el-tag>
          </div>
        </template>
        <div class="card-body">
          <p class="world-desc">{{ world.description || '暂无描述' }}</p>
        </div>
        <template #footer>
          <div class="card-footer">
            <span class="update-time">{{ formatDate(world.updated_at) }}</span>
            <div class="actions">
              <el-button type="primary" size="small" link @click="openEditDialog(world)">
                编辑
              </el-button>
              <el-button type="danger" size="small" link @click="handleDelete(world)">
                删除
              </el-button>
            </div>
          </div>
        </template>
      </el-card>
    </div>

    <!-- 空状态 -->
    <el-empty 
      v-else-if="!loading" 
      :description="currentNovelId ? '暂无世界观设定' : '请先选择作品'"
    >
      <el-button type="primary" @click="openCreateDialog" v-if="currentNovelId">
        创建第一个世界观
      </el-button>
    </el-empty>

    <!-- 加载状态 -->
    <div class="loading-container" v-if="loading">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑世界观' : '新建世界观'"
      width="500px"
      @close="resetForm"
    >
      <el-form 
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input 
            v-model="formData.name" 
            placeholder="请输入世界观名称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="formData.category" placeholder="选择分类">
            <el-option label="规则体系" value="rules" />
            <el-option label="地理环境" value="geography" />
            <el-option label="历史背景" value="history" />
            <el-option label="文化习俗" value="culture" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="5"
            placeholder="请输入世界观描述..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import { getWorlds, createWorld, updateWorld, deleteWorld } from '@/api/modules/world'
import { getNovels } from '@/api/modules/novel'

// 状态
const novels = ref([])
const currentNovelId = ref(null)
const worlds = ref([])
const loading = ref(false)
const submitting = ref(false)
const searchKeyword = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)
const formRef = ref(null)

// 表单数据
const formData = reactive({
  name: '',
  category: 'rules',
  description: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入世界观名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  description: [
    { max: 500, message: '描述不能超过500字符', trigger: 'blur' }
  ]
}

// 分类配置
const categoryMap = {
  rules: { label: '规则体系', type: 'primary' },
  geography: { label: '地理环境', type: 'success' },
  history: { label: '历史背景', type: 'warning' },
  culture: { label: '文化习俗', type: 'info' }
}

// 计算属性：过滤后的世界观
const filteredWorlds = computed(() => {
  if (!searchKeyword.value) return worlds.value
  const keyword = searchKeyword.value.toLowerCase()
  return worlds.value.filter(world => 
    world.name?.toLowerCase().includes(keyword) ||
    world.description?.toLowerCase().includes(keyword)
  )
})

// 获取作品列表
const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.data || []
    // 自动选择第一个作品
    if (novels.value.length && !currentNovelId.value) {
      currentNovelId.value = novels.value[0].id
      loadWorlds()
    }
  } catch (err) {
    console.error('加载作品列表失败:', err)
  }
}

// 加载世界观列表
const loadWorlds = async () => {
  if (!currentNovelId.value) return
  loading.value = true
  try {
    const res = await getWorlds(currentNovelId.value)
    worlds.value = res.data || []
  } catch (err) {
    console.error('加载世界观列表失败:', err)
    ElMessage.error('加载世界观失败')
  } finally {
    loading.value = false
  }
}

// 作品切换
const handleNovelChange = () => {
  loadWorlds()
}

// 搜索
const handleSearch = () => {
  // 过滤在computed中处理
}

// 获取分类标签
const getCategoryLabel = (category) => {
  return categoryMap[category]?.label || category
}

// 获取分类颜色
const getCategoryType = (category) => {
  return categoryMap[category]?.type || 'info'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

// 打开创建对话框
const openCreateDialog = () => {
  isEdit.value = false
  editingId.value = null
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (world) => {
  isEdit.value = true
  editingId.value = world.id
  formData.name = world.name
  formData.category = world.category || 'rules'
  formData.description = world.description || ''
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  formData.name = ''
  formData.category = 'rules'
  formData.description = ''
  formRef.value?.resetFields()
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateWorld(currentNovelId.value, editingId.value, {
        name: formData.name,
        category: formData.category,
        description: formData.description
      })
      ElMessage.success('更新成功')
    } else {
      await createWorld(currentNovelId.value, {
        name: formData.name,
        category: formData.category,
        description: formData.description
      })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadWorlds()
  } catch (err) {
    console.error('保存失败:', err)
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

// 删除世界观
const handleDelete = async (world) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除世界观「${world.name}」吗？`,
      '删除确认',
      { type: 'warning' }
    )
    await deleteWorld(currentNovelId.value, world.id)
    ElMessage.success('删除成功')
    loadWorlds()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 初始化
onMounted(() => {
  loadNovels()
})
</script>

<style scoped>
.worlds-page {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.novel-select {
  width: 200px;
}

.search-input {
  width: 240px;
}

.world-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.world-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.world-card:hover {
  transform: translateY(-4px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.world-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.card-body {
  min-height: 60px;
}

.world-desc {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.update-time {
  font-size: 12px;
  color: #999;
}

.actions {
  display: flex;
  gap: 8px;
}

.loading-container {
  padding: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-left {
    flex-direction: column;
  }
  
  .novel-select,
  .search-input {
    width: 100%;
  }
  
  .world-grid {
    grid-template-columns: 1fr;
  }
}
</style>
