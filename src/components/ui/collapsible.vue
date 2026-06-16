<template>
  <CollapsibleRoot :open="open" @update:open="$emit('update:open', $event)">
    <slot />
  </CollapsibleRoot>
</template>

<script setup>
import { CollapsibleRoot, CollapsibleContent, CollapsibleTrigger } from 'radix-vue'

defineProps({
  open: Boolean
})

defineEmits(['update:open'])
</script>
