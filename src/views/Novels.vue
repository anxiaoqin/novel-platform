<template>
  <div class="novels-page">
    <div class="header">
      <h2>我的作品</h2>
      <el-button type="primary" @click="handleCreate">创建新作品</el-button>
    </div>
    <el-row :gutter="20">
      <el-col :span="8" v-for="novel in novels" :key="novel.id">
        <el-card class="novel-card" shadow="hover" @click="goDetail(novel.id)">
          <h3>{{ novel.title }}</h3>
          <p class="synopsis">{{ novel.synopsis || '暂无简介' }}</p>
          <div class="meta">
            <span>字数：{{ novel.word_count || 0 }}</span>
            <span>状态：{{ novel.status || '创作中' }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="!novels.length" description="暂无作品，点击创建第一本小说" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const novels = ref([])

const loadNovels = async () => {
  try {
    const res = await api.get('/novels')
    novels.value = res.items || []
  } catch (err) {
    console.error(err)
  }
}

const handleCreate = () => {
  router.push('/home/novels?action=create')
}

const goDetail = (id) => {
  router.push(`/home/novels/${id}`)
}

onMounted(loadNovels)
</script>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.novel-card { cursor: pointer; margin-bottom: 20px; }
.novel-card h3 { margin-bottom: 8px; }
.synopsis { color: #666; font-size: 14px; margin-bottom: 12px; height: 40px; overflow: hidden; }
.meta { display: flex; justify-content: space-between; font-size: 12px; color: #999; }
</style>
