<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-3">
      <Button variant="ghost" size="sm" @click="router.push('/home/novels')">
        <ArrowLeft class="mr-1 h-4 w-4" /> 返回
      </Button>
      <h1 class="text-xl font-bold flex-1">{{ novel.title || '加载中...' }}</h1>
      <Button @click="openNewChapter">
        <Plus class="mr-1 h-4 w-4" /> 新章节
      </Button>
    </div>

    <!-- Info Card -->
    <Card>
      <CardContent class="pt-6">
        <div class="grid gap-4 sm:grid-cols-3">
          <div class="space-y-1">
            <p class="text-sm text-muted-foreground">字数</p>
            <p class="text-2xl font-bold">{{ wordCount.toLocaleString() }}</p>
          </div>
          <div class="space-y-1">
            <p class="text-sm text-muted-foreground">章节数</p>
            <p class="text-2xl font-bold">{{ chapters.length }}</p>
          </div>
          <div class="space-y-1">
            <p class="text-sm text-muted-foreground">状态</p>
            <Badge :variant="statusVariant(novel.status)">{{ statusText(novel.status) }}</Badge>
          </div>
        </div>
        <Separator class="my-4" />
        <p class="text-sm text-muted-foreground">{{ novel.description || '暂无简介' }}</p>
        <div class="mt-3 flex items-center gap-2">
          <Badge v-if="novel.genre" variant="outline">{{ novel.genre }}</Badge>
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="ghost" size="sm"><MoreHorizontal class="h-4 w-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem @click="handleCopyNovel"><Copy class="mr-2 h-4 w-4" />复制作品</DropdownMenuItem>
              <DropdownMenuItem @click="handleExportNovel"><Download class="mr-2 h-4 w-4" />导出TXT</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem @click="handleDeleteNovel" class="text-destructive"><Trash2 class="mr-2 h-4 w-4" />删除作品</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardContent>
    </Card>

    <!-- Chapters -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">章节列表</CardTitle>
      </CardHeader>
      <CardContent>
        <div v-if="!chapters.length" class="py-8 text-center text-muted-foreground">
          暂无章节，点击右上角添加
        </div>
        <div v-else class="space-y-1">
          <div
            v-for="(ch, i) in chapters"
            :key="ch.id"
            class="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-accent/50 transition-colors group"
          >
            <span class="text-sm text-muted-foreground w-8">{{ ch.order || i + 1 }}</span>
            <span class="flex-1 text-sm truncate">{{ ch.title }}</span>
            <span class="text-xs text-muted-foreground">{{ (ch.content || '').replace(/<[^>]*>/g, '').length }} 字</span>
            <Button variant="ghost" size="sm" @click="editChapter(ch)">写作</Button>
            <Button variant="ghost" size="sm" class="opacity-0 group-hover:opacity-100 text-destructive" @click="deleteChapter(ch)">删除</Button>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getNovel, deleteNovel } from '@/api/modules/novel'
import { getChapters, deleteChapter as deleteChapterApi } from '@/api/modules/chapter'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator } from '@/components/ui/dropdown-menu'
import { ArrowLeft, Plus, MoreHorizontal, Copy, Download, Trash2 } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const novel = ref({})
const chapters = ref([])

const wordCount = computed(() => chapters.value.reduce((sum, ch) => sum + (ch.content ? ch.content.replace(/<[^>]*>/g, '').length : 0), 0))
const statusText = (s) => ({ draft: '草稿', writing: '创作中', completed: '已完结' })[s] || '草稿'
const statusVariant = (s) => ({ draft: 'outline', writing: 'default', completed: 'secondary' })[s] || 'outline'

const loadNovel = async () => { try { const res = await getNovel(route.params.id); novel.value = res.data || res } catch {} }
const loadChapters = async () => { try { const res = await getChapters(route.params.id); chapters.value = res.data?.items || res.data || res || [] } catch { chapters.value = [] } }

const handleCopyNovel = async () => { /* copy not yet implemented */ }
const handleExportNovel = async () => {
  try {
    let txt = `# ${novel.value.title}\n\n`
    if (novel.value.description) txt += `## 简介\n${novel.value.description}\n\n`
    txt += '='.repeat(40) + '\n\n'
    for (let i = 0; i < chapters.value.length; i++) {
      txt += `## 第${i + 1}章 ${chapters.value[i].title}\n\n`
      txt += (chapters.value[i].content || '').replace(/<[^>]*>/g, '').trim() + '\n\n'
    }
    const blob = new Blob([txt], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = novel.value.title + '.txt'; a.click()
    URL.revokeObjectURL(url)
  } catch {}
}
const handleDeleteNovel = async () => {
  if (!confirm(`确定删除作品「${novel.value.title}」吗？此操作不可恢复！`)) return
  try { await deleteNovel(novel.value.id); router.push('/home/novels') } catch {}
}

const openNewChapter = () => { /* Will navigate to writing workspace */ router.push(`/home/novels/${route.params.id}`) }
const editChapter = (chapter) => { router.push('/write/' + route.params.id + '/' + chapter.id) }
const deleteChapter = async (chapter) => {
  if (!confirm(`确定删除章节「${chapter.title}」吗？`)) return
  try { await deleteChapterApi(chapter.id); loadChapters() } catch {}
}

onMounted(() => { loadNovel(); loadChapters() })
</script>
