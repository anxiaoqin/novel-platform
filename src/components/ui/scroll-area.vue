<template>
  <ScrollAreaRoot :class="['relative overflow-hidden', class]">
    <ScrollAreaViewport class="h-full w-full rounded-[inherit]">
      <slot />
    </ScrollAreaViewport>
    <ScrollAreaScrollbar :orientation="orientation">
      <ScrollAreaThumb class="relative flex-1 rounded-full bg-border" />
    </ScrollAreaScrollbar>
    <ScrollAreaCorner />
  </ScrollAreaRoot>
</template>

<script setup>
import { ScrollAreaRoot, ScrollAreaViewport, ScrollAreaScrollbar, ScrollAreaThumb, ScrollAreaCorner } from 'radix-vue'

defineProps({
  orientation: {
    type: String,
    default: 'vertical'
  },
  class: String
})
</script>
