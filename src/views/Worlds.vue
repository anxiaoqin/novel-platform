<template>
  <div class="worlds-page">
    <div class="header">
      <h2>世界观管理</h2>
      <el-button type="primary" @click="handleCreate">创建世界观</el-button>
    </div>
    <el-row :gutter="20">
      <el-col :span="12" v-for="world in worlds" :key="world.id">
        <el-card class="world-card">
          <template #header>
            <div class="card-header">
              <span>{{ world.name }}</span>
              <el-tag :type="world.genre === 'sci-fi' ? 'primary' : 'success'">
                {{ world.genre === 'sci-fi' ? '科幻' : '奇幻' }}
              </el-tag>
            </div>
          </template>
          <p>{{ world.description || '暂无描述' }}</p>
          <div class="card-footer">
            <span>设定数：{{ world.setting_count || 0 }}</span>
            <el-button type="primary" size="small" @click="handleEdit(world)">编辑</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="!worlds.length" description="暂无世界观，创建第一个世界观开始你的创作" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const worlds = ref([])

const handleCreate = () => {
  ElMessage.info('创建世界观功能开发中')
}

const handleEdit = (world) => {
  ElMessage.info('编辑世界观功能开发中')
}
</script>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.world-card { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
</style>
