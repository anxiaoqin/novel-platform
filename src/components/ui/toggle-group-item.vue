<template>
  <ToggleGroupItem :value="value" :class="['inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all hover:bg-muted-foreground/10 hover:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=on]:bg-background data-[state=on]:text-foreground data-[state=on]:shadow']">
    <slot />
  </ToggleGroupItem>
</template>

<script setup>
import { ToggleGroupItem } from 'radix-vue'

defineProps({ value: String })
</script>
