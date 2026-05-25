<template>
  <el-container class="home-container">
    <el-aside width="200px">
      <div class="logo">网文创作平台</div>
      <el-menu :default-active="$route.path" router>
        <el-menu-item index="/home/novels">
          <span>📚 作品管理</span>
        </el-menu-item>
        <el-menu-item index="/home/worlds">
          <span>🌍 世界观</span>
        </el-menu-item>
        <el-menu-item index="/home/characters">
          <span>👥 角色库</span>
        </el-menu-item>
        <el-menu-item index="/home/ai-write">
          <span>✍️ AI写作</span>
        </el-menu-item>
        <el-menu-item index="/home/publish">
          <span>📤 发布管理</span>
        </el-menu-item>
        <el-menu-item index="/home/settings">
          <span>⚙️ 设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-right">
          <span>{{ authStore.user?.username || '用户' }}</span>
          <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.home-container { height: 100vh; }
.el-aside { background: #304156; }
.logo { height: 60px; line-height: 60px; text-align: center; color: #fff; font-size: 18px; font-weight: bold; }
.el-menu { border: none; background: #304156; }
.el-menu-item { color: #bfcbd9; }
.el-menu-item:hover, .el-menu-item.is-active { background: #263445; color: #409eff; }
.el-header { display: flex; align-items: center; justify-content: flex-end; border-bottom: 1px solid #e6e6e6; }
.header-right { display: flex; align-items: center; gap: 16px; }
</style>
