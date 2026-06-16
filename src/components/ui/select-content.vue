<template>
  <SelectPortal>
    <SelectContent class="relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md" :side-offset="4">
      <SelectViewport class="p-1">
        <slot />
      </SelectViewport>
    </SelectContent>
  </SelectPortal>
</template>

<script setup>
import { SelectPortal, SelectContent, SelectViewport } from 'radix-vue'
</script>
