<template>
  <div class="flex min-h-screen w-full">
    <slot />
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'

const open = ref(true)
const collapsed = ref(false)

const toggle = () => { open.value = !open.value }
const toggleCollapse = () => { collapsed.value = !collapsed.value }

provide('sidebar:open', open)
provide('sidebar:toggle', toggle)
provide('sidebar:collapsed', collapsed)
provide('sidebar:toggleCollapse', toggleCollapse)
</script>
