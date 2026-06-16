<template>
  <thead :class="['[&_tr]:border-b', class]">
    <slot />
  </thead>
</template>

<script setup>
defineProps({ class: String })
</script>
