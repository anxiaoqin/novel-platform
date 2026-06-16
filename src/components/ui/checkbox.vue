<template>
  <input type="checkbox" :checked="checked" @change="$emit('update:checked', $event.target.checked)" :class="checkboxClasses" />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  checked: Boolean,
  class: String
})

defineEmits(['update:checked'])

const checkboxClasses = computed(() => {
  return `peer h-4 w-4 shrink-0 rounded-sm border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground ${props.class || ''}`
})
</script>
