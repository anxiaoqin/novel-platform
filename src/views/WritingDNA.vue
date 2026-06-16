<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">写作DNA</h1>
      <Button @click="analyzeDNA" :loading="analyzing"><Dna class="mr-2 h-4 w-4" /> 分析我的风格</Button>
    </div>

    <div v-if="dnaData" class="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle class="text-base">风格画像</CardTitle>
        </CardHeader>
        <CardContent class="space-y-3">
          <div v-for="(item, key) in dnaData.style" :key="key" class="flex items-center gap-3">
            <span class="text-sm text-muted-foreground w-20">{{ item.label }}</span>
            <div class="flex-1 h-2 rounded-full bg-secondary">
              <div class="h-2 rounded-full bg-primary transition-all" :style="{ width: item.value + '%' }" />
            </div>
            <span class="text-xs text-muted-foreground w-8 text-right">{{ item.value }}%</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle class="text-base">常用特征</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="flex flex-wrap gap-2">
            <Badge v-for="tag in dnaData.tags" :key="tag" variant="secondary">{{ tag }}</Badge>
          </div>
        </CardContent>
      </Card>
    </div>

    <div v-else class="flex flex-col items-center py-20 text-muted-foreground">
      <Dna class="h-12 w-12 mb-4" />
      <p class="text-lg font-medium">尚未分析写作风格</p>
      <p class="text-sm mt-1">点击上方按钮，AI将提取你的写作DNA</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Dna } from 'lucide-vue-next'

const dnaData = ref(null)
const analyzing = ref(false)

const analyzeDNA = async () => {
  analyzing.value = true
  try {
    // Mock DNA data - will be replaced with real API call
    await new Promise(r => setTimeout(r, 2000))
    dnaData.value = {
      style: [
        { label: '对话密度', value: 65 },
        { label: '描写深度', value: 40 },
        { label: '节奏速度', value: 75 },
        { label: '情感浓度', value: 55 },
        { label: '叙事距离', value: 30 },
      ],
      tags: ['第三人称', '多线叙事', '爽文节奏', '对话驱动', '快节奏推进']
    }
  } catch {} finally { analyzing.value = false }
}
</script>
