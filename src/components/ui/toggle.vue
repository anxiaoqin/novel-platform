<template>
  <button :class="toggleClasses" :pressed="pressed" @click="$emit('update:pressed', !pressed)">
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  pressed: Boolean,
  variant: {
    type: String,
    default: 'default'
  },
  size: {
    type: String,
    default: 'default'
  },
  disabled: Boolean,
  class: String
})

defineEmits(['update:pressed'])

const toggleClasses = computed(() => {
  const base = 'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors hover:bg-muted hover:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50'
  const active = props.pressed ? 'bg-muted' : ''
  const variants = props.variant === 'outline' ? 'border border-input shadow-sm hover:bg-accent hover:text-accent-foreground' : ''
  const sizes = props.size === 'sm' ? 'h-8 px-2' : props.size === 'lg' ? 'h-10 px-3' : 'h-9 px-2.5'
  return `${base} ${active} ${variants} ${sizes} ${props.class || ''}`
})
</script>
