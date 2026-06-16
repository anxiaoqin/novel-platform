<template>
  <textarea :class="textareaClasses" :placeholder="placeholder" :disabled="disabled" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: [String, Number],
  placeholder: String,
  disabled: Boolean,
  class: String
})

defineEmits(['update:modelValue'])

const textareaClasses = computed(() => {
  return `flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 ${props.class || ''}`
})
</script>
