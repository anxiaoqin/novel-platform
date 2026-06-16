<template>
  <div>
    <button
      :class="[
        'flex items-center gap-3 overflow-hidden rounded-md px-3 py-2 text-sm font-medium transition-colors w-full',
        isActive ? 'bg-accent text-accent-foreground' : 'text-sidebar-text hover:bg-accent/50 hover:text-foreground',
        collapsed && 'justify-center px-2'
      ]"
      @click="expanded = !expanded"
    >
      <slot name="icon" />
      <span v-if="!collapsed" class="flex-1 text-left"><slot name="title" /></span>
      <ChevronRight v-if="!collapsed" :class="['h-4 w-4 ml-auto transition-transform', expanded && 'rotate-90']" />
    </button>
    <div v-if="expanded && !collapsed" class="ml-4 mt-0.5 space-y-0.5 border-l border-border pl-3">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  childrenPaths: { type: Array, default: () => [] }
})

const route = useRoute()
const collapsed = inject('sidebar:collapsed')
const expanded = ref(false)

const isActive = computed(() => {
  return props.childrenPaths.some(p => route.path.startsWith(p))
})
</script>
