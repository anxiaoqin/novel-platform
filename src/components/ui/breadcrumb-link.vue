<template>
  <component :is="to ? 'router-link' : 'span'" :to="to" :class="['transition-colors hover:text-foreground', to ? 'hover:underline' : '']">
    <slot />
  </component>
</template>

<script setup>
defineProps({ to: String })
</script>
