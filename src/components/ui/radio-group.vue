<template>
  <RadioGroupRoot :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" :class="['grid gap-2', class]">
    <slot />
  </RadioGroupRoot>
</template>

<script setup>
import { RadioGroupRoot } from 'radix-vue'

defineProps({
  modelValue: String,
  class: String
})

defineEmits(['update:modelValue'])
</script>
