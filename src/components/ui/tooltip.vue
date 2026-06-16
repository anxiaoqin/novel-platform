<template>
  <TooltipProvider>
    <TooltipRoot :open="open" @update:open="$emit('update:open', $event)" :delay-duration="100">
      <TooltipTrigger as-child>
        <slot name="trigger" />
      </TooltipTrigger>
      <TooltipPortal>
        <TooltipContent :side="side" :class="['z-50 overflow-hidden rounded-md bg-primary px-3 py-1.5 text-xs text-primary-foreground animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2']">
          <slot />
        </TooltipContent>
      </TooltipPortal>
    </TooltipRoot>
  </TooltipProvider>
</template>

<script setup>
import { TooltipProvider, TooltipRoot, TooltipTrigger, TooltipPortal, TooltipContent } from 'radix-vue'

defineProps({
  open: Boolean,
  side: {
    type: String,
    default: 'top'
  }
})

defineEmits(['update:open'])
</script>
