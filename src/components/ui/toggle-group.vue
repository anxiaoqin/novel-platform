<template>
  <div :class="['inline-flex h-9 items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground', class]">
    <slot />
  </div>
</template>

<script setup>
defineProps({ class: String })
</script>
