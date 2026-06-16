<template>
  <SelectRoot :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)">
    <slot />
  </SelectRoot>
</template>

<script setup>
import { SelectRoot } from 'radix-vue'

defineProps({
  modelValue: String,
})

defineEmits(['update:modelValue'])
</script>
