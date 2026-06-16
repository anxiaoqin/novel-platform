<template>
  <aside
    :class="[
      'flex flex-col border-r border-border bg-sidebar-bg transition-all duration-300 shrink-0',
      collapsed ? 'w-14' : 'w-56',
      !open && 'hidden md:flex'
    ]"
  >
    <slot />
  </aside>
</template>

<script setup>
import { inject } from 'vue'

const open = inject('sidebar:open')
const collapsed = inject('sidebar:collapsed')
</script>
