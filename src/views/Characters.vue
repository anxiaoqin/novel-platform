<template>
  <div class="characters-page">
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
        <el-select 
          v-model="filterRoleType" 
          placeholder="角色类型" 
          class="role-filter"
          clearable
          @change="handleFilterChange"
        >
          <el-option label="主角" value="protagonist" />
          <el-option label="配角" value="supporting" />
          <el-option label="反派" value="antagonist" />
          <el-option label="NPC" value="npc" />
        </el-select>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索角色..."
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
        新建角色
      </el-button>
    </div>

    <!-- 主内容区：左侧列表 + 右侧详情 -->
    <div class="main-content" v-if="currentNovelId">
      <!-- 左侧角色列表 -->
      <div class="character-list">
        <div 
          v-for="char in filteredCharacters" 
          :key="char.id"
          class="character-item"
          :class="{ active: selectedCharacter?.id === char.id }"
          @click="selectCharacter(char)"
        >
          <div class="char-avatar">
            {{ char.name?.charAt(0) || '?' }}
          </div>
          <div class="char-info">
            <div class="char-name">{{ char.name }}</div>
            <el-tag :type="getRoleTypeColor(char.role_type)" size="small">
              {{ getRoleTypeLabel(char.role_type) }}
            </el-tag>
          </div>
        </div>
        
        <el-empty v-if="!filteredCharacters.length && !loading" description="暂无角色" />
        
        <div class="loading-container" v-if="loading">
          <el-skeleton :rows="3" animated />
        </div>
      </div>

      <!-- 右侧角色详情 -->
      <div class="character-detail" v-if="selectedCharacter">
        <el-card>
          <template #header>
            <div class="detail-header">
              <div class="detail-title">
                <span class="name">{{ selectedCharacter.name }}</span>
                <el-tag :type="getRoleTypeColor(selectedCharacter.role_type)">
                  {{ getRoleTypeLabel(selectedCharacter.role_type) }}
                </el-tag>
              </div>
              <div class="detail-actions">
                <el-button type="primary" link @click="openEditDialog(selectedCharacter)">
                  编辑
                </el-button>
                <el-button type="danger" link @click="handleDelete(selectedCharacter)">
                  删除
                </el-button>
              </div>
            </div>
          </template>
          
          <div class="detail-content">
            <!-- 基本信息 -->
            <div class="detail-section">
              <h4>基本信息</h4>
              <div class="info-grid">
                <div class="info-item" v-if="selectedCharacter.description">
                  <label>角色描述</label>
                  <p>{{ selectedCharacter.description }}</p>
                </div>
                <div class="info-item" v-if="selectedCharacter.appearance">
                  <label>外貌特征</label>
                  <p>{{ selectedCharacter.appearance }}</p>
                </div>
                <div class="info-item" v-if="selectedCharacter.abilities">
                  <label>能力设定</label>
                  <p>{{ selectedCharacter.abilities }}</p>
                </div>
                <div class="info-item" v-if="selectedCharacter.background">
                  <label>背景故事</label>
                  <p>{{ selectedCharacter.background }}</p>
                </div>
              </div>
            </div>

            <!-- 经典台词 -->
            <div class="detail-section" v-if="selectedCharacter.classic_quotes?.length">
              <h4>经典台词</h4>
              <div class="quotes-list">
                <div 
                  v-for="(quote, idx) in selectedCharacter.classic_quotes" 
                  :key="idx"
                  class="quote-item"
                >
                  <span class="quote-mark">"</span>
                  {{ quote }}
                </div>
              </div>
            </div>

            <!-- 角色标签 -->
            <div class="detail-section" v-if="selectedCharacter.tags?.length">
              <h4>角色标签</h4>
              <div class="tags-list">
                <el-tag v-for="tag in selectedCharacter.tags" :key="tag" size="small">
                  {{ tag }}
                </el-tag>
              </div>
            </div>

            <!-- 成长线 -->
            <div class="detail-section" v-if="selectedCharacter.growth_line?.length">
              <h4>成长线</h4>
              <el-timeline>
                <el-timeline-item
                  v-for="(growth, idx) in selectedCharacter.growth_line"
                  :key="idx"
                  :timestamp="`第${growth.chapter}章`"
                  placement="top"
                >
                  <el-card>
                    <h5>{{ growth.event }}</h5>
                    <p>{{ growth.description }}</p>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </div>

            <!-- 关系图谱 -->
            <div class="detail-section" v-if="relationships.length">
              <h4>关系图谱</h4>
              <div class="relationships-list">
                <div 
                  v-for="rel in relationships" 
                  :key="`${rel.source_id}-${rel.target_id}`"
                  class="relationship-item"
                >
                  <span class="rel-source">{{ rel.source_name }}</span>
                  <span class="rel-arrow">→</span>
                  <span class="rel-target">{{ rel.target_name }}</span>
                  <el-tag size="small" type="info">{{ rel.relation }}</el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
      
      <el-empty v-else description="选择角色查看详情" />
    </div>

    <el-empty v-else description="请先选择作品" />

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑角色' : '新建角色'"
      width="700px"
      @close="resetForm"
    >
      <el-form 
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="90px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="角色名" prop="name">
              <el-input v-model="formData.name" placeholder="请输入角色名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色类型" prop="role_type">
              <el-select v-model="formData.role_type" placeholder="选择类型">
                <el-option label="主角" value="protagonist" />
                <el-option label="配角" value="supporting" />
                <el-option label="反派" value="antagonist" />
                <el-option label="NPC" value="npc" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="角色描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="2" placeholder="简要描述" />
        </el-form-item>
        
        <el-form-item label="外貌特征" prop="appearance">
          <el-input v-model="formData.appearance" type="textarea" :rows="2" placeholder="描述外貌" />
        </el-form-item>
        
        <el-form-item label="能力设定" prop="abilities">
          <el-input v-model="formData.abilities" type="textarea" :rows="2" placeholder="描述能力" />
        </el-form-item>
        
        <el-form-item label="背景故事" prop="background">
          <el-input v-model="formData.background" type="textarea" :rows="3" placeholder="角色背景" />
        </el-form-item>
        
        <el-form-item label="经典台词">
          <div class="quotes-input">
            <el-input 
              v-model="newQuote" 
              placeholder="输入台词后点击添加"
              @keyup.enter="addQuote"
            >
              <template #append>
                <el-button @click="addQuote">添加</el-button>
              </template>
            </el-input>
            <div class="quotes-tags" v-if="formData.classic_quotes.length">
              <el-tag
                v-for="(q, idx) in formData.classic_quotes"
                :key="idx"
                closable
                @close="removeQuote(idx)"
              >
                {{ q }}
              </el-tag>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="角色标签">
          <div class="tags-input">
            <el-input 
              v-model="newTag" 
              placeholder="输入标签后点击添加"
              @keyup.enter="addTag"
            >
              <template #append>
                <el-button @click="addTag">添加</el-button>
              </template>
            </el-input>
            <div class="tags-wrap" v-if="formData.tags.length">
              <el-tag
                v-for="(t, idx) in formData.tags"
                :key="idx"
                closable
                @close="removeTag(idx)"
              >
                {{ t }}
              </el-tag>
            </div>
          </div>
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
import { 
  getCharacters, 
  createCharacter, 
  updateCharacter, 
  deleteCharacter,
  getCharacterRelationships 
} from '@/api/modules/character'
import { getNovels } from '@/api/modules/novel'

// 状态
const novels = ref([])
const currentNovelId = ref(null)
const characters = ref([])
const selectedCharacter = ref(null)
const relationships = ref([])
const loading = ref(false)
const submitting = ref(false)
const filterRoleType = ref('')
const searchKeyword = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)
const formRef = ref(null)

// 新台词/标签
const newQuote = ref('')
const newTag = ref('')

// 表单数据
const formData = reactive({
  name: '',
  role_type: 'protagonist',
  description: '',
  appearance: '',
  abilities: '',
  background: '',
  classic_quotes: [],
  tags: []
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入角色名', trigger: 'blur' }
  ],
  role_type: [
    { required: true, message: '请选择角色类型', trigger: 'change' }
  ]
}

// 角色类型配置
const roleTypeMap = {
  protagonist: { label: '主角', color: 'danger' },
  supporting: { label: '配角', color: 'warning' },
  antagonist: { label: '反派', color: 'info' },
  npc: { label: 'NPC', color: '' }
}

// 计算属性：过滤后的角色
const filteredCharacters = computed(() => {
  let result = characters.value
  
  if (filterRoleType.value) {
    result = result.filter(c => c.role_type === filterRoleType.value)
  }
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(c => 
      c.name?.toLowerCase().includes(keyword) ||
      c.description?.toLowerCase().includes(keyword)
    )
  }
  
  return result
})

// 获取作品列表
const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.data || []
    if (novels.value.length && !currentNovelId.value) {
      currentNovelId.value = novels.value[0].id
      loadCharacters()
    }
  } catch (err) {
    console.error('加载作品列表失败:', err)
  }
}

// 加载角色列表
const loadCharacters = async () => {
  if (!currentNovelId.value) return
  loading.value = true
  try {
    const params = {}
    if (filterRoleType.value) {
      params.type = filterRoleType.value
    }
    const res = await getCharacters(currentNovelId.value, params)
    characters.value = res.data || []
    // 如果有选中的角色，更新详情
    if (selectedCharacter.value) {
      selectedCharacter.value = characters.value.find(c => c.id === selectedCharacter.value.id)
    }
  } catch (err) {
    console.error('加载角色列表失败:', err)
    ElMessage.error('加载角色失败')
  } finally {
    loading.value = false
  }
}

// 加载关系图谱
const loadRelationships = async () => {
  if (!currentNovelId.value) return
  try {
    const res = await getCharacterRelationships(currentNovelId.value)
    relationships.value = res.data?.relationships || []
  } catch (err) {
    console.error('加载关系图谱失败:', err)
  }
}

// 作品切换
const handleNovelChange = () => {
  selectedCharacter.value = null
  loadCharacters()
  loadRelationships()
}

// 筛选变化
const handleFilterChange = () => {
  loadCharacters()
}

// 搜索
const handleSearch = () => {
  // 过滤在computed中处理
}

// 选择角色
const selectCharacter = (char) => {
  selectedCharacter.value = char
}

// 获取角色类型标签
const getRoleTypeLabel = (type) => {
  return roleTypeMap[type]?.label || type
}

// 获取角色类型颜色
const getRoleTypeColor = (type) => {
  return roleTypeMap[type]?.color || ''
}

// 添加台词
const addQuote = () => {
  if (newQuote.value.trim()) {
    formData.classic_quotes.push(newQuote.value.trim())
    newQuote.value = ''
  }
}

// 移除台词
const removeQuote = (idx) => {
  formData.classic_quotes.splice(idx, 1)
}

// 添加标签
const addTag = () => {
  if (newTag.value.trim() && !formData.tags.includes(newTag.value.trim())) {
    formData.tags.push(newTag.value.trim())
    newTag.value = ''
  }
}

// 移除标签
const removeTag = (idx) => {
  formData.tags.splice(idx, 1)
}

// 打开创建对话框
const openCreateDialog = () => {
  isEdit.value = false
  editingId.value = null
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (char) => {
  isEdit.value = true
  editingId.value = char.id
  formData.name = char.name
  formData.role_type = char.role_type || 'protagonist'
  formData.description = char.description || ''
  formData.appearance = char.appearance || ''
  formData.abilities = char.abilities || ''
  formData.background = char.background || ''
  formData.classic_quotes = [...(char.classic_quotes || [])]
  formData.tags = [...(char.tags || [])]
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  formData.name = ''
  formData.role_type = 'protagonist'
  formData.description = ''
  formData.appearance = ''
  formData.abilities = ''
  formData.background = ''
  formData.classic_quotes = []
  formData.tags = []
  newQuote.value = ''
  newTag.value = ''
  formRef.value?.resetFields()
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    const payload = {
      name: formData.name,
      role_type: formData.role_type,
      description: formData.description,
      appearance: formData.appearance,
      abilities: formData.abilities,
      background: formData.background,
      classic_quotes: formData.classic_quotes,
      tags: formData.tags
    }
    
    if (isEdit.value) {
      await updateCharacter(currentNovelId.value, editingId.value, payload)
      ElMessage.success('更新成功')
    } else {
      await createCharacter(currentNovelId.value, payload)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadCharacters()
  } catch (err) {
    console.error('保存失败:', err)
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

// 删除角色
const handleDelete = async (char) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除角色「${char.name}」吗？`,
      '删除确认',
      { type: 'warning' }
    )
    await deleteCharacter(currentNovelId.value, char.id)
    ElMessage.success('删除成功')
    if (selectedCharacter.value?.id === char.id) {
      selectedCharacter.value = null
    }
    loadCharacters()
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
.characters-page {
  padding: 20px;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.novel-select {
  width: 180px;
}

.role-filter {
  width: 120px;
}

.search-input {
  width: 200px;
}

.main-content {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* 角色列表 */
.character-list {
  width: 280px;
  flex-shrink: 0;
  overflow-y: auto;
  padding-right: 8px;
}

.character-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 8px;
  background: var(--bg-secondary, #f5f7fa);
}

.character-item:hover {
  background: var(--bg-hover, #ecf5ff);
}

.character-item.active {
  background: var(--brand-primary-light, #e6f0ff);
  border-left: 3px solid var(--brand-primary, #409eff);
}

.char-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.char-info {
  flex: 1;
  min-width: 0;
}

.char-name {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 角色详情 */
.character-detail {
  flex: 1;
  overflow-y: auto;
  min-width: 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-title .name {
  font-size: 18px;
  font-weight: 600;
}

.detail-content {
  max-height: calc(100vh - 280px);
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  font-size: 14px;
  color: #999;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.info-grid {
  display: grid;
  gap: 16px;
}

.info-item label {
  font-size: 12px;
  color: #666;
  display: block;
  margin-bottom: 4px;
}

.info-item p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-primary);
}

.quotes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quote-item {
  position: relative;
  padding: 12px 16px;
  background: #f9f9f9;
  border-radius: 8px;
  font-style: italic;
  color: #555;
}

.quote-mark {
  font-size: 24px;
  color: #ddd;
  margin-right: 4px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.relationships-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.relationship-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f9f9f9;
  border-radius: 6px;
}

.rel-source, .rel-target {
  font-weight: 500;
}

.rel-arrow {
  color: #999;
}

/* 标签输入 */
.quotes-input, .tags-input {
  width: 100%;
}

.quotes-tags, .tags-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.loading-container {
  padding: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .character-list {
    width: 100%;
    max-height: 200px;
  }
}
</style>
