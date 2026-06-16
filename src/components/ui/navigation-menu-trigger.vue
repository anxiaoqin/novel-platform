<template>
  <NavigationMenuTrigger :class="['group inline-flex h-9 w-max items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-muted hover:text-accent-foreground focus:bg-muted focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-muted data-[state=open]:bg-muted data-[state=open]:text-accent-foreground']">
    <slot />
    <span class="i-lucide-chevron-down h-3 w-3 transition-transform group-data-[state=open]:rotate-180 ml-1" />
  </NavigationMenuTrigger>
</template>

<script setup>
import { NavigationMenuTrigger } from '@radix-ui/vue-navigation-menu'
</script>
