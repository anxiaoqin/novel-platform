<template>
  <div class="publish-page">
    <h2>多平台发布</h2>
    <el-row :gutter="20">
      <el-col :span="8" v-for="platform in platforms" :key="platform.id">
        <el-card class="platform-card">
          <div class="platform-icon">{{ platform.icon }}</div>
          <h3>{{ platform.name }}</h3>
          <p>{{ platform.description }}</p>
          <el-tag :type="platform.status === 'bound' ? 'success' : 'info'">
            {{ platform.status === 'bound' ? '已绑定' : '未绑定' }}
          </el-tag>
          <div style="margin-top: 12px">
            <el-button v-if="platform.status !== 'bound'" type="primary" size="small">
              绑定账号
            </el-button>
            <el-button v-else type="success" size="small">
              管理作品
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const platforms = ref([
  { id: 1, name: '番茄小说', icon: '🍅', description: '字节跳动旗下免费小说平台', status: 'unbound' },
  { id: 2, name: '起点中文网', icon: '📚', description: '阅文集团旗舰平台', status: 'unbound' },
  { id: 3, name: '飞卢小说网', icon: '✈️', description: '主打同人/轻小说', status: 'unbound' },
  { id: 4, name: '七猫小说', icon: '🐱', description: '免费阅读平台', status: 'unbound' },
  { id: 5, name: '晋江文学城', icon: '🌸', description: '女性向文学平台', status: 'unbound' },
  { id: 6, name: '纵横中文网', icon: '📖', description: '完美世界旗下', status: 'unbound' }
])
</script>

<style scoped>
.platform-card { text-align: center; margin-bottom: 20px; }
.platform-icon { font-size: 48px; margin-bottom: 12px; }
</style>
