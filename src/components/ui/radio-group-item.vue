<template>
  <RadioGroupItem :value="value" :class="['aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50']">
    <RadioGroupIndicator class="flex h-full w-full items-center justify-center rounded-full bg-primary" />
  </RadioGroupItem>
</template>

<script setup>
import { RadioGroupItem, RadioGroupIndicator } from 'radix-vue'

defineProps({ value: String })
</script>
