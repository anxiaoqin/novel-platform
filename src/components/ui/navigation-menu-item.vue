<template>
  <NavigationMenuItem :class="['relative', class]">
    <slot />
  </NavigationMenuItem>
</template>

<script setup>
import { NavigationMenuItem } from '@radix-ui/vue-navigation-menu'
defineProps({ class: String })
</script>
