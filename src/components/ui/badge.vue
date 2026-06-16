<template>
  <component :is="as" :class="badgeClasses">
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'secondary', 'destructive', 'outline'].includes(v)
  },
  as: {
    type: String,
    default: 'span'
  },
  class: String
})

const badgeClasses = computed(() => {
  const base = 'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2'
  
  const variants = {
    default: 'border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80',
    secondary: 'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
    destructive: 'border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/90',
    outline: 'text-foreground'
  }
  
  return `${base} ${variants[props.variant]} ${props.class || ''}`
})
</script>
