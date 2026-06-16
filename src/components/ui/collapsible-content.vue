<template>
  <CollapsibleContent class="overflow-hidden transition-all data-[state=closed]:animate-collapsible-up data-[state=open]:animate-collapsible-down">
    <slot />
  </CollapsibleContent>
</template>

<script setup>
import { CollapsibleContent } from 'radix-vue'
</script>
