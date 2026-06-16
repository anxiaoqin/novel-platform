<template>
  <TabsRoot :default-value="defaultValue" :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" class="w-full">
    <slot />
  </TabsRoot>
</template>

<script setup>
import { TabsRoot } from 'radix-vue'
defineProps({ defaultValue: String, modelValue: String })
defineEmits(['update:modelValue'])
</script>
