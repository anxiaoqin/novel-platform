<template>
  <Sidebar>
    <!-- Header / Logo -->
    <div class="flex h-12 items-center border-b border-border px-3 shrink-0">
      <span class="text-lg">📖</span>
      <span v-if="!collapsed" class="ml-2 text-sm font-bold text-foreground truncate">十方书社</span>
      <button
        v-if="!collapsed"
        class="ml-auto flex h-6 w-6 items-center justify-center rounded hover:bg-accent transition-colors"
        @click="toggleCollapse"
      >
        <ChevronsLeft class="h-3.5 w-3.5 text-muted-foreground" />
      </button>
    </div>

    <!-- Menu -->
    <div class="flex-1 overflow-y-auto py-2">
      <SidebarMenu>
        <SidebarMenuItem v-for="item in menuItems" :key="item.label">
          <!-- 子菜单项 -->
          <template v-if="item.children">
            <SidebarMenuSub :children-paths="item.children.map(c => c.path)">
              <template #icon>
                <component :is="item.icon" class="h-4 w-4 shrink-0" />
              </template>
              <template #title>{{ item.label }}</template>
              <SidebarMenuItem v-for="child in item.children" :key="child.path">
                <SidebarMenuButton :to="child.path">
                  <component :is="child.icon" class="h-4 w-4 shrink-0" />
                  <span v-if="!collapsed">{{ child.label }}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenuSub>
          </template>
          <!-- 普通菜单项 -->
          <template v-else>
            <SidebarMenuButton :to="item.path">
              <component :is="item.icon" class="h-4 w-4 shrink-0" />
              <span v-if="!collapsed">{{ item.label }}</span>
            </SidebarMenuButton>
          </template>
        </SidebarMenuItem>
      </SidebarMenu>
    </div>

    <!-- Footer / Settings -->
    <div class="border-t border-border p-2 shrink-0">
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton to="/home/settings">
            <Settings class="h-4 w-4 shrink-0" />
            <span v-if="!collapsed">设置</span>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </div>
  </Sidebar>
</template>

<script setup>
import { inject } from 'vue'
import { BookOpen, Globe, Users, Clock, Dna, PenTool, Settings, ChevronRight, ChevronsLeft } from 'lucide-vue-next'
import Sidebar from '@/components/ui/sidebar.vue'
import SidebarMenu from '@/components/ui/sidebar-menu.vue'
import SidebarMenuItem from '@/components/ui/sidebar-menu-item.vue'
import SidebarMenuButton from '@/components/ui/sidebar-menu-button.vue'
import SidebarMenuSub from '@/components/ui/sidebar-menu-sub.vue'

const collapsed = inject('sidebar:collapsed')
const toggleCollapse = inject('sidebar:toggleCollapse')

const menuItems = [
  { path: '/home/novels', label: '作品管理', icon: BookOpen },
  {
    label: '素材设定库', icon: Globe,
    children: [
      { path: '/home/worlds', label: '世界观', icon: Globe },
      { path: '/home/characters', label: '角色库', icon: Users },
      { path: '/home/timeline', label: '时间线', icon: Clock },
    ]
  },
  { path: '/home/writing-dna', label: '写作DNA', icon: Dna },
  { path: '/home/ai-write', label: 'AI写作', icon: PenTool },
]
</script>
