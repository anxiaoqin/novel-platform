<template>
  <DropdownMenuTrigger as-child>
    <slot />
  </DropdownMenuTrigger>
</template>

<script setup>
import { DropdownMenuTrigger } from 'radix-vue'
</script>
