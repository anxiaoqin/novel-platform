<template>
  <div class="space-y-6">
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <CardTitle class="text-base">AI事件分析</CardTitle>
          <Button @click="runAnalysis" :loading="analyzing" size="sm">
            <Sparkles class="mr-1 h-4 w-4" /> 开始分析
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="events.length" class="space-y-3">
          <div v-for="(event, i) in events" :key="i"
            class="flex items-start gap-3 rounded-lg border border-border p-3 hover:bg-accent/50 transition-colors cursor-pointer"
            :class="{ 'border-primary bg-accent': event.selected }"
            @click="event.selected = !event.selected"
          >
            <Checkbox :checked="event.selected" @update:checked="event.selected = $event" @click.stop />
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <Badge :variant="eventTypeVariant(event.type)" class="text-xs">{{ event.type }}</Badge>
                <span class="font-medium text-sm">{{ event.title }}</span>
              </div>
              <p class="text-xs text-muted-foreground mt-1">{{ event.description }}</p>
            </div>
          </div>
        </div>
        <div v-else-if="analyzing" class="flex flex-col items-center py-8">
          <div class="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          <p class="mt-3 text-sm text-muted-foreground">AI正在分析灵感中的故事事件...</p>
        </div>
        <div v-else class="py-8 text-center text-muted-foreground">
          <p class="text-sm">点击"开始分析"，AI将提取故事事件建议</p>
        </div>
      </CardContent>
    </Card>

    <div class="flex justify-between">
      <Button variant="outline" @click="$emit('prev')">上一步</Button>
      <Button @click="$emit('next')" :disabled="!selectedEvents.length">
        选择{{ selectedEvents.length }}个事件，下一步 <ArrowRight class="ml-1 h-4 w-4" />
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import { ArrowRight, Sparkles } from 'lucide-vue-next'

const emit = defineEmits(['next', 'prev'])

const events = ref([])
const analyzing = ref(false)

const selectedEvents = computed(() => events.value.filter(e => e.selected))

const eventTypeVariant = (type) => {
  const map = { 人物: 'default', 冲突: 'destructive', 转折: 'secondary', 伏笔: 'outline', 情节: 'default', 环境: 'outline' }
  return map[type] || 'outline'
}

const runAnalysis = async () => {
  analyzing.value = true
  try {
    await new Promise(r => setTimeout(r, 2000))
    events.value = [
      { title: '主角觉醒', type: '转折', description: '少年在矿难中意外激活上古传承', selected: true },
      { title: '宗门追杀', type: '冲突', description: '传承暴露，引来宗门觊觎', selected: false },
      { title: '神秘老者', type: '人物', description: '途中遇到的前辈，暗藏身份', selected: true },
      { title: '遗迹试炼', type: '情节', description: '进入上古遗迹接受考验', selected: false },
      { title: '身世之谜', type: '伏笔', description: '传承中闪过的画面暗示主角身世', selected: true },
    ]
  } finally { analyzing.value = false }
}
</script>
