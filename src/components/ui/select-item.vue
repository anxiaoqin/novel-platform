<template>
  <SelectItem :value="value" :disabled="disabled" class="relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50">
    <slot />
    <span class="absolute right-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectItemIndicator>
        <span class="i-lucide-check h-4 w-4" />
      </SelectItemIndicator>
    </span>
  </SelectItem>
</template>

<script setup>
import { SelectItem, SelectItemIndicator } from 'radix-vue'

defineProps({
  value: String,
  disabled: Boolean
})
</script>
