<template>
  <component
    :is="as"
    :to="as === 'router-link' ? to : undefined"
    :class="[
      'flex items-center gap-3 overflow-hidden rounded-md px-3 py-2 text-sm font-medium transition-colors w-full',
      isActive ? 'bg-accent text-accent-foreground' : 'text-sidebar-text hover:bg-accent/50 hover:text-foreground',
      collapsed && 'justify-center px-2'
    ]"
    @click="as === 'button' && $emit('click')"
  >
    <slot />
  </component>
</template>

<script setup>
import { computed, inject } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  as: { type: String, default: 'router-link' },
  to: String,
  isActive: Boolean
})

const route = useRoute()
const collapsed = inject('sidebar:collapsed')

const isActive = computed(() => {
  if (props.isActive !== undefined) return props.isActive
  return props.to ? route.path.startsWith(props.to) : false
})
</script>
