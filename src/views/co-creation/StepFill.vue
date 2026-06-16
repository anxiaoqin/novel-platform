<template>
  <div class="space-y-6">
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <CardTitle class="text-base">AI正文填充</CardTitle>
          <Button @click="runFill" :loading="filling" size="sm">
            <Sparkles class="mr-1 h-4 w-4" /> 开始填充
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="generatedContent" class="prose prose-sm max-w-none text-foreground whitespace-pre-wrap rounded-lg border border-border p-4">
          {{ generatedContent }}
        </div>
        <div v-else-if="filling" class="flex flex-col items-center py-12">
          <div class="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          <p class="mt-3 text-sm text-muted-foreground">AI正在按大纲填充正文...</p>
        </div>
        <div v-else class="py-8 text-center text-muted-foreground">
          <p class="text-sm">点击"开始填充"，AI将按大纲生成正文</p>
        </div>
      </CardContent>
    </Card>

    <div class="flex justify-between">
      <Button variant="outline" @click="$emit('prev')">上一步</Button>
      <Button @click="$emit('done')" :disabled="!generatedContent">
        完成，进入编辑 <Check class="ml-1 h-4 w-4" />
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Check, Sparkles } from 'lucide-vue-next'

defineEmits(['next', 'prev', 'done'])

const generatedContent = ref('')
const filling = ref(false)

const runFill = async () => {
  filling.value = true
  generatedContent.value = ''
  try {
    // Simulate streaming
    const text = '矿洞深处，少年林天被巨石压住双腿，意识逐渐模糊。\n\n就在这生死一线之际，一道金光从石缝中透出，直冲他的眉心。刹那间，无数画面如洪流般涌入脑海——\n\n上古修士的修炼记忆，天地灵气的运转法则，还有一段模糊却震撼的画面：一个身影立于万族之巅，回眸时，面容竟与自己一般无二。\n\n"这......是什么？"\n\n林天猛然睁眼，浑身经脉中涌入一股温热的力量，压在身上的巨石竟被轻而易举地推开。'
    for (let i = 0; i < text.length; i += 3) {
      generatedContent.value += text.slice(i, i + 3)
      await new Promise(r => setTimeout(r, 30))
    }
  } finally { filling.value = false }
}
</script>
