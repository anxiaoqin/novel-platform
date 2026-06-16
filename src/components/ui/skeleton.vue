<template>
  <div :class="['animate-pulse rounded-md bg-muted', class]" />
</template>

<script setup>
defineProps({
  class: String
})
</script>
