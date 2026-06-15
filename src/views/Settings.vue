<template>
  <div class="settings-page">
    <h2>设置</h2>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本设置" name="basic">
        <el-card>
          <el-form label-width="120px">
            <el-form-item label="主题">
              <el-radio-group v-model="settings.theme">
                <el-radio label="light">浅色</el-radio>
                <el-radio label="dark">深色</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="自动保存">
              <el-switch v-model="settings.autoSave" />
            </el-form-item>
            <el-form-item label="保存间隔">
              <el-input-number v-model="settings.autoSaveInterval" :min="10" :max="300" :step="10" />
              <span style="margin-left: 8px">秒</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="AI配置" name="ai">
        <el-card>
          <el-form label-width="120px">
            <el-form-item label="AI服务商">
              <el-select v-model="settings.aiProvider" style="width: 200px">
                <el-option label="扣子 Coze" value="coze" />
                <el-option label="通义千问" value="qwen" />
                <el-option label="自定义API" value="custom" />
              </el-select>
            </el-form-item>
            <el-form-item v-if="settings.aiProvider === 'coze'" label="扣子API Token">
              <el-input v-model="settings.cozeToken" type="password" show-password style="width: 300px" />
            </el-form-item>
            <el-form-item v-if="settings.aiProvider === 'qwen'" label="通义千问Key">
              <el-input v-model="settings.qwenKey" type="password" show-password style="width: 300px" />
            </el-form-item>
            <el-form-item v-if="settings.aiProvider === 'custom'" label="自定义API地址">
              <el-input v-model="settings.customApiUrl" style="width: 300px" placeholder="https://api.example.com/v1" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveSettings">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="账号安全" name="security">
        <el-card>
          <el-form label-width="120px">
            <el-form-item label="当前账号">
              <span>{{ authStore.user?.username }}</span>
            </el-form-item>
            <el-form-item label="修改密码">
              <el-input type="password" style="width: 200px" placeholder="新密码" />
            </el-form-item>
            <el-form-item>
              <el-button type="danger" @click="handleLogout">退出登录</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const activeTab = ref('basic')

const settings = reactive({
  theme: 'light',
  autoSave: true,
  autoSaveInterval: 30,
  aiProvider: 'coze',
  cozeToken: '',
  qwenKey: '',
  customApiUrl: ''
})

const saveSettings = () => {
  localStorage.setItem('settings', JSON.stringify(settings))
  ElMessage.success('设置已保存')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
</style>
