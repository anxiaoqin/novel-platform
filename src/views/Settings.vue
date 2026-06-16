<template>
  <div class="mx-auto max-w-2xl space-y-6">
    <h1 class="text-2xl font-bold">设置</h1>

    <!-- 账号信息 -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">账号信息</CardTitle>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-muted-foreground">用户名</p>
            <p class="font-medium">{{ authStore.user?.username || '未登录' }}</p>
          </div>
          <Button variant="outline" size="sm">修改密码</Button>
        </div>
      </CardContent>
    </Card>

    <!-- 偏好设置 -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">偏好设置</CardTitle>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium">暗色模式</p>
            <p class="text-sm text-muted-foreground">切换界面主题</p>
          </div>
          <div class="flex gap-1">
            <button
              v-for="t in themes"
              :key="t.value"
              class="flex h-8 w-8 items-center justify-center rounded-md text-sm transition-colors hover:bg-accent"
              :class="{ 'bg-accent text-accent-foreground': currentTheme === t.value }"
              @click="handleThemeChange(t.value)"
            >{{ t.icon }}</button>
          </div>
        </div>
        <Separator />
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium">自动保存</p>
            <p class="text-sm text-muted-foreground">编辑器自动保存草稿</p>
          </div>
          <Switch :checked="settings.autoSave" @update:checked="settings.autoSave = $event" />
        </div>
      </CardContent>
    </Card>

    <!-- AI 配置 -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">AI配置</CardTitle>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="space-y-2">
          <Label>AI服务商</Label>
          <Select v-model="settings.aiProvider">
            <SelectTrigger class="w-[200px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="coze">扣子 Coze</SelectItem>
              <SelectItem value="qwen">通义千问</SelectItem>
              <SelectItem value="custom">自定义API</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>

    <!-- 数据 -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">数据与存储</CardTitle>
      </CardHeader>
      <CardContent class="space-y-3">
        <Button variant="outline" size="sm">导出所有数据</Button>
        <div class="flex gap-2">
          <Button variant="outline" size="sm" @click="saveSettings">保存设置</Button>
          <Button variant="destructive" size="sm" @click="handleLogout">退出登录</Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme, THEMES } from '@/composables/useTheme'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'

const router = useRouter()
const authStore = useAuthStore()
const { theme: currentTheme, setTheme } = useTheme()
const themes = THEMES

const settings = reactive({
  theme: 'dark',
  autoSave: true,
  aiProvider: 'coze',
})

const handleThemeChange = (t) => setTheme(t)
const saveSettings = () => { localStorage.setItem('settings', JSON.stringify(settings)) }
const handleLogout = () => { authStore.logout(); router.push('/login') }
</script>
