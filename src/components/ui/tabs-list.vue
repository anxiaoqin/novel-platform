<template>
  <TabsList class="inline-flex h-9 items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground">
    <slot />
  </TabsList>
</template>

<script setup>
import { TabsList } from 'radix-vue'
</script>
