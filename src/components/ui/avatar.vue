<template>
  <component :is="as" :class="avatarClasses">
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  as: {
    type: String,
    default: 'div'
  },
  class: String
})

const avatarClasses = computed(() => {
  return `relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full ${props.class || ''}`
})
</script>
