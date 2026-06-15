<template>
  <el-container class="home-container">
    <!-- 侧边栏 -->
    <el-aside width="220px">
      <div class="logo">📚 十方书社</div>
      <el-menu 
        :default-active="activeMenu" 
        router 
        class="sidebar-menu"
        background-color="#1a1a2e"
        text-color="#a0a0a0"
        active-text-color="#667eea"
      >
        <!-- 作品管理 -->
        <el-menu-item index="/home/novels">
          <span class="menu-icon">📚</span>
          <span>作品管理</span>
        </el-menu-item>

        <!-- 素材设定库 - 二级菜单 -->
        <el-sub-menu index="/home/materials">
          <template #title>
            <span class="menu-icon">🌍</span>
            <span>素材设定库</span>
          </template>
          <el-menu-item index="/home/worlds">
            <span class="sub-menu-icon">🌐</span>
            <span>世界观</span>
          </el-menu-item>
          <el-menu-item index="/home/characters">
            <span class="sub-menu-icon">👥</span>
            <span>角色库</span>
          </el-menu-item>
          <el-menu-item index="/home/timeline">
            <span class="sub-menu-icon">⏰</span>
            <span>时间线</span>
          </el-menu-item>
        </el-sub-menu>

        <!-- 写作DNA -->
        <el-menu-item index="/home/writing-dna">
          <span class="menu-icon">🧬</span>
          <span>写作DNA</span>
        </el-menu-item>

        <!-- 人机共创 -->
        <el-menu-item index="/home/ai-write">
          <span class="menu-icon">✍️</span>
          <span>AI写作</span>
        </el-menu-item>

        <!-- 发布管理 -->
        <el-menu-item index="/home/publish">
          <span class="menu-icon">📤</span>
          <span>发布管理</span>
        </el-menu-item>

        <!-- 设置 -->
        <el-menu-item index="/home/settings">
          <span class="menu-icon">⚙️</span>
          <span>设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <el-header>
        <div class="header-left">
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <div class="user-info">
            <span class="username">{{ authStore.user?.username || '用户' }}</span>
            <el-dropdown @command="handleCommand">
              <el-avatar :size="32" class="user-avatar">
                {{ (authStore.user?.username || 'U').charAt(0).toUpperCase() }}
              </el-avatar>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="settings">个人设置</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 当前激活的菜单
const activeMenu = computed(() => {
  const path = route.path
  // 精确匹配
  if (route.meta?.menuPath) return route.meta.menuPath
  // 子菜单激活
  if (path.startsWith('/home/worlds')) return '/home/worlds'
  if (path.startsWith('/home/characters')) return '/home/characters'
  if (path.startsWith('/home/timeline')) return '/home/timeline'
  return path
})

// 页面标题
const pageTitle = computed(() => {
  const path = route.path
  const titles = {
    '/home/novels': '我的作品',
    '/home/worlds': '世界观设定',
    '/home/characters': '角色库',
    '/home/timeline': '时间线',
    '/home/writing-dna': '写作DNA',
    '/home/ai-write': 'AI写作',
    '/home/co-creation': '人机共创',
    '/home/publish': '发布管理',
    '/home/settings': '系统设置'
  }
  // 匹配作品详情
  if (path.match(/^\/home\/novels\/\d+$/)) return '作品详情'
  return titles[path] || '十方书社'
})

// 下拉菜单命令
const handleCommand = (command) => {
  switch (command) {
    case 'settings':
      router.push('/home/settings')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 退出登录
const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  height: 100vh;
  background: var(--bg-primary, #f5f7fa);
}

.el-aside {
  background: #1a1a2e;
  overflow-x: hidden;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  letter-spacing: 2px;
}

.sidebar-menu {
  border: none;
  background: #1a1a2e;
}

.sidebar-menu .el-menu-item,
.sidebar-menu .el-sub-menu__title {
  height: 50px;
  line-height: 50px;
  padding-left: 20px !important;
  transition: all 0.3s;
}

.sidebar-menu .el-menu-item:hover,
.sidebar-menu .el-sub-menu__title:hover {
  background: rgba(102, 126, 234, 0.1) !important;
}

.sidebar-menu .el-menu-item.is-active {
  background: rgba(102, 126, 234, 0.15) !important;
  border-left: 3px solid #667eea;
}

.menu-icon {
  margin-right: 10px;
  font-size: 16px;
}

.sub-menu-icon {
  margin-right: 8px;
  font-size: 14px;
}

/* 子菜单样式 */
:deep(.el-sub-menu .el-menu) {
  background: #16162a !important;
}

:deep(.el-sub-menu .el-menu-item) {
  height: 44px;
  line-height: 44px;
  padding-left: 50px !important;
  font-size: 13px;
}

:deep(.el-sub-menu .el-menu-item:hover) {
  background: rgba(102, 126, 234, 0.1) !important;
}

:deep(.el-sub-menu .el-menu-item.is-active) {
  background: rgba(102, 126, 234, 0.15) !important;
}

/* Header */
.el-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: #666;
  font-size: 14px;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
}

/* Main */
.el-main {
  padding: 20px;
  overflow-y: auto;
}

/* 响应式 */
@media (max-width: 768px) {
  .el-aside {
    width: 60px !important;
  }
  
  .logo {
    font-size: 0;
    padding: 0;
  }
  
  .logo::before {
    content: '📚';
    font-size: 20px;
  }
  
  .sidebar-menu .el-menu-item span,
  .sidebar-menu .el-sub-menu__title span:not(.menu-icon) {
    display: none;
  }
  
  .sidebar-menu .el-sub-menu .el-menu-item {
    padding-left: 20px !important;
  }
}
</style>
