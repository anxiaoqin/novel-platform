<template>
  <div :class="['flex items-center justify-center gap-1', class]">
    <Button variant="outline" size="icon" :disabled="modelValue <= 1" @click="$emit('update:modelValue', modelValue - 1)">
      <span class="i-lucide-chevron-left h-4 w-4" />
    </Button>
    <template v-for="page in pages" :key="page">
      <span v-if="page === '...'" class="px-2">...</span>
      <Button v-else :variant="modelValue === page ? 'default' : 'outline'" size="icon" @click="$emit('update:modelValue', page)">
        {{ page }}
      </Button>
    </template>
    <Button variant="outline" size="icon" :disabled="modelValue >= totalPages" @click="$emit('update:modelValue', modelValue + 1)">
      <span class="i-lucide-chevron-right h-4 w-4" />
    </Button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: Number,
  totalPages: Number,
  class: String
})

defineEmits(['update:modelValue'])

const pages = computed(() => {
  const result = []
  const total = props.totalPages
  const current = props.modelValue
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) result.push(i)
  } else {
    if (current <= 3) {
      result.push(1, 2, 3, 4, '...', total)
    } else if (current >= total - 2) {
      result.push(1, '...', total - 3, total - 2, total - 1, total)
    } else {
      result.push(1, '...', current - 1, current, current + 1, '...', total)
    }
  }
  return result
})
</script>
