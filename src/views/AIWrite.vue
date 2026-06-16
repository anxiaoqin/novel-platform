<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">AI写作助手</h1>
      <Select :model-value="currentNovelId" @update:model-value="currentNovelId = $event">
        <SelectTrigger class="w-[200px]">
          <SelectValue placeholder="选择作品" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem v-for="novel in novels" :key="novel.id" :value="novel.id">{{ novel.title }}</SelectItem>
        </SelectContent>
      </Select>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle class="text-base">AI功能</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="grid gap-3 sm:grid-cols-2">
            <Button variant="outline" class="justify-start h-auto py-3" @click="aiMode = 'continue'">
              <span class="text-lg mr-2">✨</span>
              <div class="text-left"><p class="font-medium">智能续写</p><p class="text-xs text-muted-foreground">3个候选续写方案</p></div>
            </Button>
            <Button variant="outline" class="justify-start h-auto py-3" @click="aiMode = 'polish'">
              <span class="text-lg mr-2">💎</span>
              <div class="text-left"><p class="font-medium">润色优化</p><p class="text-xs text-muted-foreground">提升文字质量</p></div>
            </Button>
            <Button variant="outline" class="justify-start h-auto py-3" @click="aiMode = 'deai'">
              <span class="text-lg mr-2">🎭</span>
              <div class="text-left"><p class="font-medium">去AI味</p><p class="text-xs text-muted-foreground">让文字回归人味</p></div>
            </Button>
            <Button variant="outline" class="justify-start h-auto py-3" @click="aiMode = 'inspire'">
              <span class="text-lg mr-2">💡</span>
              <div class="text-left"><p class="font-medium">灵感生成</p><p class="text-xs text-muted-foreground">打破写作瓶颈</p></div>
            </Button>
          </div>
          <Separator />
          <div class="space-y-2">
            <Label>输入内容</Label>
            <Textarea v-model="inputText" placeholder="在此输入需要AI处理的内容..." :rows="6" />
            <Button class="w-full" :loading="aiLoading" @click="runAI">开始生成</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle class="text-base">生成结果</CardTitle>
        </CardHeader>
        <CardContent>
          <div v-if="aiResult" class="prose prose-sm max-w-none text-foreground whitespace-pre-wrap">{{ aiResult }}</div>
          <div v-else class="flex flex-col items-center justify-center py-12 text-muted-foreground">
            <PenTool class="h-8 w-8 mb-3" />
            <p class="text-sm">选择AI功能并输入内容，结果将在此显示</p>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getNovels } from '@/api/modules/novel'
import { fillChapterStream, extractContent } from '@/api/sse'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { PenTool } from 'lucide-vue-next'

const novels = ref([])
const currentNovelId = ref(null)
const inputText = ref('')
const aiResult = ref('')
const aiLoading = ref(false)
const aiMode = ref('continue')

const runAI = async () => {
  if (!inputText.value) return
  aiLoading.value = true
  aiResult.value = ''
  try {
    fillChapterStream(
      { text: inputText.value, mode: aiMode.value, novel_id: currentNovelId.value },
      {
        onMessage: (data) => {
          const content = extractContent(data)
          if (content) aiResult.value += content
        },
        onDone: () => { aiLoading.value = false },
        onError: () => { aiLoading.value = false }
      }
    )
  } catch (e) {
    aiLoading.value = false
  }
}

onMounted(async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.data || []
    if (novels.value.length) currentNovelId.value = novels.value[0].id
  } catch (e) {
    console.error('加载作品失败:', e)
  }
})
</script>
