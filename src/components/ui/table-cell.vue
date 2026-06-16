<template>
  <td :class="['p-2 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]', class]">
    <slot />
  </td>
</template>

<script setup>
defineProps({ class: String })
</script>
