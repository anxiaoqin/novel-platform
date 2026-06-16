<template>
  <DialogRoot :open="open" @update:open="$emit('update:open', $event)">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 z-50" />
      <DialogContent :class="['fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 duration-200', sideClasses]">
        <slot />
        <DialogClose class="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
          <span class="i-lucide-x h-4 w-4" />
        </DialogClose>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<script setup>
import { computed } from 'vue'
import { DialogRoot, DialogPortal, DialogOverlay, DialogContent, DialogClose } from 'radix-vue'

const props = defineProps({
  open: Boolean,
  side: {
    type: String,
    default: 'right'
  }
})

defineEmits(['update:open'])

const sideClasses = computed(() => {
  const sides = {
    top: 'inset-x-0 top-0 border-b max-h-[85vh] w-full rounded-b-lg',
    bottom: 'inset-x-0 bottom-0 border-t max-h-[85vh] w-full rounded-t-lg',
    left: 'inset-y-0 left-0 h-full w-3/4 max-w-sm border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left',
    right: 'inset-y-0 right-0 h-full w-3/4 max-w-sm border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right'
  }
  return sides[props.side] || sides.right
})
</script>
