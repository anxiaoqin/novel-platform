<template>
  <div class="novels-page">
    <div class="header">
      <h2>我的作品</h2>
      <el-button type="primary" @click="showCreateDialog = true">创建新作品</el-button>
    </div>
    
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="8" v-for="novel in novels" :key="novel.id">
        <el-card class="novel-card" shadow="hover" @click="goDetail(novel.id)">
          <h3>{{ novel.title }}</h3>
          <p class="synopsis">{{ novel.description || '暂无简介' }}</p>
          <div class="meta">
            <span>字数：{{ novel.word_count || 0 }}</span>
            <span :class="statusClass(novel.status)">{{ statusText(novel.status) }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-empty v-if="!novels.length" description="暂无作品，点击创建第一本小说" />

    <!-- 创建作品对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建新作品" width="520px" :close-on-click-modal="false">
      <el-form :model="createForm" :rules="formRules" ref="formRef" label-width="80px">
        <el-form-item label="作品名称" prop="title">
          <el-input v-model="createForm.title" placeholder="请输入作品名称" maxlength="50" show-word-limit />
        </el-form-item>
        <el-form-item label="类型" prop="genre">
          <el-select v-model="createForm.genre" placeholder="选择作品类型" style="width:100%">
            <el-option v-for="g in genres" :key="g" :label="g" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="createForm.description" type="textarea" :rows="3" placeholder="简要描述你的作品" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item label="写作风格">
          <el-input v-model="createForm.writing_style" placeholder="如：古风、轻松、热血" />
        </el-form-item>
        <el-form-item label="核心创意">
          <el-input v-model="createForm.core_idea" placeholder="一句话概括核心卖点" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" :loading="creating" @click="handleCreateSubmit">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getNovels, createNovel } from '@/api/modules/novel'

const router = useRouter()
const novels = ref([])
const showCreateDialog = ref(false)
const creating = ref(false)
const formRef = ref(null)

const genres = ['玄幻', '仙侠', '都市', '科幻', '历史', '悬疑', '言情', '游戏', '体育', '军事', '奇幻', '武侠', '其他']

const createForm = ref({
  title: '',
  genre: '',
  description: '',
  writing_style: '',
  core_idea: ''
})

const formRules = {
  title: [{ required: true, message: '请输入作品名称', trigger: 'blur' }],
  genre: [{ required: true, message: '请选择作品类型', trigger: 'change' }]
}

const statusText = (status) => {
  const map = { draft: '草稿', writing: '创作中', completed: '已完结' }
  return map[status] || '草稿'
}

const statusClass = (status) => {
  const map = { draft: 'status-draft', writing: 'status-writing', completed: 'status-done' }
  return map[status] || 'status-draft'
}

const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.items || res.data || []
  } catch (err) {
    console.error('加载作品列表失败:', err)
  }
}

const handleCreateSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch { return }
  
  creating.value = true
  try {
    const res = await createNovel(createForm.value)
    ElMessage.success('作品创建成功')
    showCreateDialog.value = false
    // 重置表单
    createForm.value = { title: '', genre: '', description: '', writing_style: '', core_idea: '' }
    // 重新加载列表
    await loadNovels()
    // 跳转到新作品详情
    const newId = res.data?.id || res.id
    if (newId) {
      router.push(`/home/novels/${newId}`)
    }
  } catch (err) {
    ElMessage.error(err.response?.data?.error || '创建失败，请重试')
  } finally {
    creating.value = false
  }
}

const goDetail = (id) => {
  router.push(`/home/novels/${id}`)
}

onMounted(loadNovels)
</script>

<style scoped>
.novels-page { padding: 24px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.header h2 { margin: 0; }
.novel-card { cursor: pointer; margin-bottom: 20px; transition: transform 0.2s; }
.novel-card:hover { transform: translateY(-2px); }
.novel-card h3 { margin-bottom: 8px; font-size: 16px; }
.synopsis { color: var(--text-secondary, #666); font-size: 14px; margin-bottom: 12px; height: 40px; overflow: hidden; }
.meta { display: flex; justify-content: space-between; font-size: 12px; color: var(--text-tertiary, #999); }
.status-draft { color: var(--color-info, #909399); }
.status-writing { color: var(--color-primary, #409eff); }
.status-done { color: var(--color-success, #67c23a); }
</style>
