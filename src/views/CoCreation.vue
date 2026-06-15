<template>
  <div class="co-creation-page">
    <div class="header">
      <h2>🤝 人机共创</h2>
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
    
    <el-card class="intro-card">
      <template #header>
        <span class="card-title">共创流程说明</span>
      </template>
      <div class="steps-intro">
        <div class="step-item">
          <div class="step-num">1</div>
          <div class="step-content">
            <h4>世界观设定</h4>
            <p>构建故事发生的世界背景、规则体系、地理环境等</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">2</div>
          <div class="step-content">
            <h4>角色设计</h4>
            <p>创建故事中的主要角色，包括主角、配角、反派等</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">3</div>
          <div class="step-content">
            <h4>事件规划</h4>
            <p>设计故事的关键事件和发展脉络</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">4</div>
          <div class="step-content">
            <h4>正文创作</h4>
            <p>AI辅助下的正文写作与优化</p>
          </div>
        </div>
      </div>
    </el-card>

    <div class="action-cards">
      <el-card class="action-card" shadow="hover" @click="goTo('/home/worlds')">
        <div class="card-icon">🌍</div>
        <h3>世界观设定</h3>
        <p>构建世界背景与规则体系</p>
      </el-card>
      
      <el-card class="action-card" shadow="hover" @click="goTo('/home/characters')">
        <div class="card-icon">👥</div>
        <h3>角色设计</h3>
        <p>创建与管理角色设定</p>
      </el-card>
      
      <el-card class="action-card" shadow="hover" @click="goTo('/home/timeline')">
        <div class="card-icon">⏰</div>
        <h3>时间线规划</h3>
        <p>梳理故事时间脉络</p>
      </el-card>
      
      <el-card class="action-card" shadow="hover" @click="goTo('/home/ai-write')">
        <div class="card-icon">✍️</div>
        <h3>AI写作</h3>
        <p>开始正文创作</p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getNovels } from '@/api/modules/novel'

const router = useRouter()
const novels = ref([])
const currentNovelId = ref(null)

const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.data || []
    if (novels.value.length) {
      currentNovelId.value = novels.value[0].id
    }
  } catch (err) {
    console.error('加载作品列表失败:', err)
  }
}

const handleNovelChange = () => {
  // 切换作品后刷新数据
}

const goTo = (path) => {
  router.push(path)
}

onMounted(() => {
  loadNovels()
})
</script>

<style scoped>
.co-creation-page {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h2 {
  margin: 0;
  font-size: 20px;
}

.novel-select {
  width: 200px;
}

.intro-card {
  margin-bottom: 24px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}

.steps-intro {
  display: flex;
  gap: 20px;
  padding: 10px 0;
}

.step-item {
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content h4 {
  margin: 0 0 4px;
  font-size: 14px;
}

.step-content p {
  margin: 0;
  font-size: 12px;
  color: #666;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.action-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.action-card:hover {
  transform: translateY(-4px);
}

.card-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.action-card h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.action-card p {
  margin: 0;
  font-size: 13px;
  color: #666;
}

@media (max-width: 1024px) {
  .action-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .steps-intro {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .action-cards {
    grid-template-columns: 1fr;
  }
}
</style>
