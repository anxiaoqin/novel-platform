<template>
  <div class="characters-page">
    <div class="header">
      <h2>角色库</h2>
      <el-button type="primary" @click="handleCreate">创建角色</el-button>
    </div>
    <el-row :gutter="20">
      <el-col :span="8" v-for="char in characters" :key="char.id">
        <el-card class="char-card">
          <div class="char-avatar">{{ char.name?.charAt(0) || '?' }}</div>
          <h3>{{ char.name }}</h3>
          <el-tag size="small">{{ char.role || '主角' }}</el-tag>
          <p class="desc">{{ char.description || '暂无描述' }}</p>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="!characters.length" description="暂无角色，创建第一个角色" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const characters = ref([])

const handleCreate = () => {
  ElMessage.info('创建角色功能开发中')
}
</script>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.char-card { text-align: center; margin-bottom: 20px; }
.char-avatar { width: 60px; height: 60px; border-radius: 50%; background: #409eff; color: #fff; font-size: 24px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; }
.desc { margin-top: 8px; color: #666; font-size: 14px; height: 40px; overflow: hidden; }
</style>
