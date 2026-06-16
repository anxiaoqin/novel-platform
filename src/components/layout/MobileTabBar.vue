<template>
  <nav class="fixed bottom-0 left-0 right-0 z-50 flex h-14 items-center justify-around border-t border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 safe-area-bottom">
    <router-link
      v-for="tab in tabs"
      :key="tab.path"
      :to="tab.path"
      class="flex flex-col items-center gap-0.5 text-[10px] transition-colors"
      :class="isActive(tab) ? 'text-primary' : 'text-muted-foreground'"
    >
      <component :is="tab.icon" class="h-5 w-5" />
      <span>{{ tab.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { BookOpen, PenTool, Users, Dna, Settings } from 'lucide-vue-next'

const route = useRoute()

const tabs = [
  { path: '/home/novels', label: '作品', icon: BookOpen },
  { path: '/home/ai-write', label: 'AI写', icon: PenTool },
  { path: '/home/characters', label: '角色', icon: Users },
  { path: '/home/writing-dna', label: 'DNA', icon: Dna },
  { path: '/home/settings', label: '设置', icon: Settings },
]

const isActive = (tab) => route.path.startsWith(tab.path)
</script>

<style scoped>
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
</style>
