<template>
  <component :is="as" :class="separatorClasses" v-bind="attrs" />
</template>

<script setup>
import { computed, useAttrs } from 'vue'

const props = defineProps({
  as: {
    type: String,
    default: 'hr'
  },
  orientation: {
    type: String,
    default: 'horizontal'
  },
  class: String
})

const attrs = useAttrs()

const separatorClasses = computed(() => {
  const base = 'shrink-0 bg-border'
  const orientation = props.orientation === 'horizontal' ? 'h-[1px] w-full' : 'h-full w-[1px]'
  return `${base} ${orientation} ${props.class || ''}`
})
</script>
