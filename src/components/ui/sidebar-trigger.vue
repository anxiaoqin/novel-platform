<template>
  <button
    class="flex h-7 w-7 items-center justify-center rounded-md hover:bg-accent transition-colors"
    @click="toggle"
    title="切换侧边栏"
  >
    <PanelLeft class="h-4 w-4 text-muted-foreground" />
  </button>
</template>

<script setup>
import { inject } from 'vue'
import { PanelLeft } from 'lucide-vue-next'
const toggle = inject('sidebar:toggle')
</script>
