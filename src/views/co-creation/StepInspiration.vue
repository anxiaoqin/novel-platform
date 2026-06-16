<template>
  <div class="space-y-6">
    <div class="grid gap-6 lg:grid-cols-2">
      <!-- 左：灵感模板 -->
      <Card>
        <CardHeader>
          <CardTitle class="text-base">灵感模板</CardTitle>
        </CardHeader>
        <CardContent class="space-y-2">
          <button
            v-for="tpl in templates"
            :key="tpl.name"
            class="w-full rounded-md border border-border px-3 py-2 text-left text-sm transition-colors hover:bg-accent"
            :class="{ 'border-primary bg-accent': selectedTemplate === tpl.name }"
            @click="selectedTemplate = tpl.name; inspiration = tpl.prompt"
          >
            <span class="font-medium">{{ tpl.icon }} {{ tpl.name }}</span>
            <p class="text-xs text-muted-foreground mt-0.5">{{ tpl.desc }}</p>
          </button>
        </CardContent>
      </Card>

      <!-- 右：输入区 -->
      <Card>
        <CardHeader>
          <CardTitle class="text-base">灵感输入</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <Textarea v-model="inspiration" placeholder="输入你的灵感——一段对话、一个场景、一个碎片..." :rows="8" />
          <div class="flex gap-2">
            <Button @click="$emit('next')" :disabled="!inspiration.trim()">
              下一步 <ArrowRight class="ml-1 h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { ArrowRight } from 'lucide-vue-next'

defineEmits(['next'])

const inspiration = ref('')
const selectedTemplate = ref('')

const templates = [
  { name: '玄幻修仙', icon: '⚔️', desc: '修炼飞升、宗门争斗', prompt: '一个少年在废弃矿脉中意外获得上古传承...' },
  { name: '都市异能', icon: '🏙️', desc: '现代都市+超能力', prompt: '一觉醒来，发现自己能看到别人的倒计时...' },
  { name: '悬疑推理', icon: '🔍', desc: '案件谜团、层层解谜', prompt: '一封来自十年后的信，写着今天的死亡预告...' },
  { name: '言情甜宠', icon: '💕', desc: '甜蜜恋爱故事', prompt: '相亲对象居然是五年前不告而别的初恋...' },
  { name: '科幻未来', icon: '🚀', desc: '太空探索、未来世界', prompt: '人类最后一批移民船抵达目标星系，却发现已有文明存在...' },
  { name: '历史架空', icon: '🏯', desc: '穿越时空、改写历史', prompt: '考古发掘出土一面铜镜，映出的不是自己的脸...' },
]
</script>
