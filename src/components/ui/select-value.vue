<template>
  <SelectValue :placeholder="placeholder" />
</template>

<script setup>
import { SelectValue } from 'radix-vue'
defineProps({ placeholder: String })
</script>
