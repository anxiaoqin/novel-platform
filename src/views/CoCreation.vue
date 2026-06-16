<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">🤝 人机共创</h1>
      <Select v-model="currentNovelId" @update:modelValue="handleNovelChange">
        <SelectTrigger class="w-[200px]">
          <SelectValue placeholder="选择作品" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem v-for="novel in novels" :key="novel.id" :value="novel.id">{{ novel.title }}</SelectItem>
        </SelectContent>
      </Select>
    </div>

    <!-- 4步流程说明 -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">共创流程说明</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="(step, i) in steps" :key="i" class="flex items-start gap-3">
            <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">
              {{ i + 1 }}
            </div>
            <div>
              <Badge variant="outline" class="text-xs mb-1">{{ step.who }}</Badge>
              <p class="font-medium text-sm">{{ step.title }}</p>
              <p class="text-xs text-muted-foreground mt-0.5">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- 功能入口卡片 -->
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <Card
        v-for="entry in entries"
        :key="entry.path"
        class="cursor-pointer transition-all hover:shadow-md hover:-translate-y-0.5"
        @click="router.push(entry.path)"
      >
        <CardContent class="pt-6 text-center">
          <span class="text-4xl">{{ entry.icon }}</span>
          <h3 class="mt-3 font-semibold">{{ entry.title }}</h3>
          <p class="mt-1 text-sm text-muted-foreground">{{ entry.desc }}</p>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getNovels } from '@/api/modules/novel'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'

const router = useRouter()
const novels = ref([])
const currentNovelId = ref(null)

const steps = [
  { who: '人', title: '灵感输入', desc: '自由写作灵感碎片' },
  { who: 'AI', title: '事件分析', desc: 'AI提取故事事件' },
  { who: '人', title: '组合大纲', desc: '挑选事件组合大纲' },
  { who: 'AI', title: '正文填充', desc: 'AI按大纲填充正文' },
]

const entries = [
  { icon: '🌍', title: '世界观设定', desc: '构建世界背景与规则', path: '/home/worlds' },
  { icon: '👥', title: '角色设计', desc: '创建与管理角色', path: '/home/characters' },
  { icon: '⏰', title: '时间线规划', desc: '梳理故事脉络', path: '/home/timeline' },
  { icon: '✍️', title: 'AI写作', desc: '开始正文创作', path: '/home/ai-write' },
]

const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.data || []
    if (novels.value.length) currentNovelId.value = novels.value[0].id
  } catch {}
}

const handleNovelChange = () => {}

onMounted(loadNovels)
</script>
