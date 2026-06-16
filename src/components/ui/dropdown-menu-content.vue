<template>
  <DropdownMenuPortal>
    <DropdownMenuContent
      :align="align"
      :side-offset="4"
      class="z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md"
    >
      <slot />
    </DropdownMenuContent>
  </DropdownMenuPortal>
</template>

<script setup>
import { DropdownMenuPortal, DropdownMenuContent } from 'radix-vue'

defineProps({
  align: { type: String, default: 'end' }
})
</script>
