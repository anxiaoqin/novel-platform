<template>
  <div :class="['relative w-full overflow-auto', class]">
    <table :class="['w-full caption-bottom text-sm', class]">
      <slot />
    </table>
  </div>
</template>

<script setup>
defineProps({ class: String })
</script>
