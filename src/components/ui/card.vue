<template>
  <component :is="as" :class="cardClasses">
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

const cardClasses = computed(() => {
  return `rounded-lg border bg-card text-card-foreground shadow-sm ${props.class || ''}`
})
</script>
