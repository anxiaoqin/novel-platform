<template>
  <SelectTrigger class="flex h-9 w-full items-center justify-between rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm" as-child>
    <button class="w-full flex items-center justify-between">
      <slot />
    </button>
  </SelectTrigger>
</template>

<script setup>
import { SelectTrigger } from 'radix-vue'
</script>
