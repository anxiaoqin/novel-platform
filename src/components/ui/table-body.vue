<template>
  <tbody :class="['[&_tr:last-child]:border-0', class]">
    <slot />
  </tbody>
</template>

<script setup>
defineProps({ class: String })
</script>
