<template>
  <div class="space-y-6">
    <Card>
      <CardHeader>
        <CardTitle class="text-base">组合大纲</CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm text-muted-foreground mb-4">拖拽调整顺序，点击编辑内容</p>
        <div class="space-y-2">
          <div v-for="(node, i) in outlineNodes" :key="i"
            class="flex items-center gap-3 rounded-lg border border-border p-3 transition-colors hover:bg-accent/50"
          >
            <span class="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">{{ i + 1 }}</span>
            <div class="flex-1 min-w-0">
              <Input v-model="node.title" class="border-0 h-7 px-1 text-sm font-medium" />
              <Textarea v-model="node.description" class="border-0 px-1 text-xs text-muted-foreground resize-none" :rows="1" />
            </div>
            <Button variant="ghost" size="icon" class="h-7 w-7 shrink-0" @click="outlineNodes.splice(i, 1)">
              <X class="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>
        <Button variant="outline" size="sm" class="mt-3" @click="outlineNodes.push({ title: '新节点', description: '' })">
          <Plus class="mr-1 h-3.5 w-3.5" /> 添加节点
        </Button>
      </CardContent>
    </Card>

    <div class="flex justify-between">
      <Button variant="outline" @click="$emit('prev')">上一步</Button>
      <Button @click="$emit('next')" :disabled="!outlineNodes.length">
        确认大纲，下一步 <ArrowRight class="ml-1 h-4 w-4" />
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { ArrowRight, Plus, X } from 'lucide-vue-next'

defineEmits(['next', 'prev'])

const outlineNodes = ref([
  { title: '主角觉醒', description: '少年在矿难中意外激活上古传承' },
  { title: '神秘老者', description: '途中遇到的前辈，暗藏身份' },
  { title: '身世之谜', description: '传承中闪过的画面暗示主角身世' },
])
</script>
