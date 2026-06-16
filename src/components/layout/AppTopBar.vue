<template>
  <header class="flex h-12 items-center gap-2 border-b border-border bg-background px-4">
    <SidebarTrigger class="-ml-1" />
    <Separator orientation="vertical" class="mr-2 h-4" />

    <h2 class="text-sm font-medium text-foreground flex-1">{{ pageTitle }}</h2>

    <div class="flex items-center gap-2">
      <!-- 主题切换 -->
      <div class="flex gap-1">
        <button
          v-for="t in themes"
          :key="t.value"
          class="flex h-7 w-7 items-center justify-center rounded text-xs transition-colors hover:bg-accent"
          :class="{ 'bg-accent text-accent-foreground': currentTheme === t.value }"
          :title="t.label"
          @click="handleThemeChange(t.value)"
        >
          {{ t.icon }}
        </button>
      </div>

      <Separator orientation="vertical" class="h-4" />

      <!-- 用户菜单 -->
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <button class="flex items-center gap-2 rounded-md px-2 py-1 text-sm hover:bg-accent transition-colors">
            <Avatar class="h-6 w-6">
              <AvatarFallback class="text-xs bg-primary text-primary-foreground">
                {{ (authStore.user?.username || 'U').charAt(0).toUpperCase() }}
              </AvatarFallback>
            </Avatar>
            <span class="hidden sm:inline text-muted-foreground">{{ authStore.user?.username || '用户' }}</span>
          </button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuLabel>我的账号</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem @click="router.push('/home/settings')">
            <Settings class="mr-2 h-4 w-4" />
            个人设置
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem @click="handleLogout" class="text-destructive">
            <LogOut class="mr-2 h-4 w-4" />
            退出登录
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme, THEMES } from '@/composables/useTheme'
import { Settings, LogOut } from 'lucide-vue-next'
import { Separator } from '@/components/ui/separator'
import { SidebarTrigger } from '@/components/ui/sidebar'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem,
  DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { theme: currentTheme, setTheme } = useTheme()
const themes = THEMES

const pageTitle = computed(() => {
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
  if (route.path.match(/^\/home\/novels\/\d+$/)) return '作品详情'
  return titles[route.path] || '十方书社'
})

const handleThemeChange = (t) => setTheme(t)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
