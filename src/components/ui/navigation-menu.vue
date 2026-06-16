<template>
  <NavigationMenuRoot :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" :class="['relative z-10 flex max-w-max flex-1 items-center justify-center', class]">
    <slot />
  </NavigationMenuRoot>
</template>

<script setup>
import { NavigationMenuRoot } from '@radix-ui/vue-navigation-menu'

defineProps({
  modelValue: String,
  class: String
})

defineEmits(['update:modelValue'])
</script>
