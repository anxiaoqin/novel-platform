<template>
  <NavigationMenuList :class="['center flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground', class]">
    <slot />
  </NavigationMenuList>
</template>

<script setup>
import { NavigationMenuList } from '@radix-ui/vue-navigation-menu'
defineProps({ class: String })
</script>
