<template>
  <tr :class="['border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted', class]">
    <slot />
  </tr>
</template>

<script setup>
defineProps({ class: String })
</script>
