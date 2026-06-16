<template>
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <AppTopBar />
      <main class="flex-1 overflow-auto p-4 md:p-6 bg-background">
        <router-view />
      </main>
      <MobileTabBar class="md:hidden" />
    </SidebarInset>
  </SidebarProvider>
</template>

<script setup>
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar'
import AppSidebar from './AppSidebar.vue'
import AppTopBar from './AppTopBar.vue'
import MobileTabBar from './MobileTabBar.vue'
</script>
