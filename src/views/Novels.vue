<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">我的作品</h1>
      <Button @click="showCreateDialog = true">
        <Plus class="mr-2 h-4 w-4" /> 创建新作品
      </Button>
    </div>

    <!-- Search & Filter -->
    <div class="flex flex-wrap gap-3">
      <div class="relative flex-1 min-w-[200px] max-w-sm">
        <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input v-model="searchQuery" placeholder="搜索作品..." class="pl-9" />
      </div>
      <Select v-model="statusFilter">
        <SelectTrigger class="w-[130px]">
          <SelectValue placeholder="全部状态" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">全部</SelectItem>
          <SelectItem value="draft">草稿</SelectItem>
          <SelectItem value="writing">创作中</SelectItem>
          <SelectItem value="completed">已完结</SelectItem>
        </SelectContent>
      </Select>
    </div>

    <!-- Novel Grid -->
    <div v-if="filteredNovels.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <Card
        v-for="novel in filteredNovels"
        :key="novel.id"
        class="cursor-pointer transition-all hover:shadow-md hover:-translate-y-0.5 group"
        @click="goDetail(novel.id)"
      >
        <CardHeader class="pb-3">
          <div class="flex items-start justify-between">
            <CardTitle class="text-base line-clamp-1">{{ novel.title }}</CardTitle>
            <DropdownMenu>
              <DropdownMenuTrigger as-child @click.stop>
                <Button variant="ghost" size="icon" class="h-7 w-7 opacity-0 group-hover:opacity-100 transition-opacity">
                  <MoreHorizontal class="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem @click.stop="goDetail(novel.id)">
                  <Pencil class="mr-2 h-4 w-4" /> 编辑信息
                </DropdownMenuItem>
                <DropdownMenuItem @click.stop="handleCopyNovel(novel)">
                  <Copy class="mr-2 h-4 w-4" /> 复制作品
                </DropdownMenuItem>
                <DropdownMenuItem @click.stop="handleExportNovel(novel)">
                  <Download class="mr-2 h-4 w-4" /> 导出TXT
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem @click.stop="handleDeleteNovel(novel)" class="text-destructive">
                  <Trash2 class="mr-2 h-4 w-4" /> 删除
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <p class="text-sm text-muted-foreground line-clamp-2">{{ novel.description || '暂无简介' }}</p>
        </CardHeader>
        <CardContent>
          <div class="flex items-center gap-2">
            <Badge :variant="statusVariant(novel.status)">{{ statusText(novel.status) }}</Badge>
            <Badge v-if="novel.genre" variant="outline">{{ novel.genre }}</Badge>
          </div>
          <div class="mt-3 flex items-center justify-between text-xs text-muted-foreground">
            <span>{{ novel.word_count || 0 }} 字</span>
            <Button variant="default" size="sm" @click.stop="goWrite(novel.id)">
              写作 <ArrowRight class="ml-1 h-3 w-3" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Empty State -->
    <div v-else class="flex flex-col items-center justify-center py-20 text-center">
      <BookOpen class="h-12 w-12 text-muted-foreground/50" />
      <p class="mt-4 text-muted-foreground">暂无作品，点击创建第一本小说</p>
      <Button class="mt-4" @click="showCreateDialog = true">
        <Plus class="mr-2 h-4 w-4" /> 创建新作品
      </Button>
    </div>

    <!-- Create Dialog -->
    <Dialog :open="showCreateDialog" @update:open="showCreateDialog = $event">
      <DialogContent class="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>创建新作品</DialogTitle>
          <DialogDescription>填写基本信息，开始你的创作之旅</DialogDescription>
        </DialogHeader>
        <form @submit.prevent="handleCreateSubmit" class="space-y-4">
          <div class="space-y-2">
            <Label for="title">作品名称 *</Label>
            <Input id="title" v-model="createForm.title" placeholder="请输入作品名称" maxlength="50" />
          </div>
          <div class="space-y-2">
            <Label for="genre">类型 *</Label>
            <Select v-model="createForm.genre">
              <SelectTrigger>
                <SelectValue placeholder="选择作品类型" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="g in genres" :key="g" :value="g">{{ g }}</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="space-y-2">
            <Label for="desc">简介</Label>
            <Textarea id="desc" v-model="createForm.description" placeholder="简要描述你的作品" :rows="3" maxlength="500" />
          </div>
          <div class="space-y-2">
            <Label for="style">写作风格</Label>
            <Input id="style" v-model="createForm.writing_style" placeholder="如：古风、轻松、热血" />
          </div>
          <div class="space-y-2">
            <Label for="idea">核心创意</Label>
            <Input id="idea" v-model="createForm.core_idea" placeholder="一句话概括核心卖点" />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" @click="showCreateDialog = false">取消</Button>
            <Button type="submit" :loading="creating">创建</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getNovels, createNovel, deleteNovel, getNovel } from '@/api/modules/novel'
import { getChapters } from '@/api/modules/chapter'
import api from '@/api'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator } from '@/components/ui/dropdown-menu'
import { Plus, Search, MoreHorizontal, Pencil, Copy, Download, Trash2, ArrowRight, BookOpen } from 'lucide-vue-next'

const router = useRouter()
const novels = ref([])
const showCreateDialog = ref(false)
const creating = ref(false)
const searchQuery = ref('')
const statusFilter = ref('all')

const genres = ['玄幻', '仙侠', '都市', '科幻', '历史', '悬疑', '言情', '游戏', '体育', '军事', '奇幻', '武侠', '其他']

const createForm = ref({ title: '', genre: '', description: '', writing_style: '', core_idea: '' })

const statusText = (s) => ({ draft: '草稿', writing: '创作中', completed: '已完结' })[s] || '草稿'
const statusVariant = (s) => ({ draft: 'outline', writing: 'default', completed: 'secondary' })[s] || 'outline'

const filteredNovels = computed(() => {
  let list = novels.value
  if (statusFilter.value !== 'all') list = list.filter(n => n.status === statusFilter.value)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(n => n.title?.toLowerCase().includes(q) || n.description?.toLowerCase().includes(q))
  }
  return list
})

const loadNovels = async () => {
  try {
    const res = await getNovels()
    novels.value = res.data?.items || res.items || res.data || []
  } catch (err) { console.error('加载作品列表失败:', err) }
}

const goDetail = (id) => router.push(`/home/novels/${id}`)
const goWrite = (id) => router.push(`/home/novels/${id}`)

const handleDeleteNovel = async (novel) => {
  if (!confirm(`确定删除作品《${novel.title}》吗？此操作不可恢复！`)) return
  try { await deleteNovel(novel.id); loadNovels() } catch (err) { console.error('删除失败:', err) }
}

const handleCopyNovel = async (novel) => {
  try { await api.post(`/novels/${novel.id}/copy`, { title: `${novel.title}（副本）` }); loadNovels() } catch (err) { console.error('复制失败:', err) }
}

const handleExportNovel = async (novel) => {
  try {
    const novelRes = await getNovel(novel.id)
    const novelData = novelRes.data || novelRes
    const chaptersRes = await getChapters(novel.id)
    const chapters = chaptersRes.data?.items || chaptersRes.data || chaptersRes || []
    let txt = `# ${novelData.title}\n\n`
    if (novelData.description) txt += `## 简介\n${novelData.description}\n\n`
    txt += '='.repeat(40) + '\n\n'
    for (let i = 0; i < chapters.length; i++) {
      const ch = chapters[i]
      txt += `## 第${i + 1}章 ${ch.title}\n\n`
      try {
        const res = await api.get(`/chapters/${ch.id}`)
        txt += (res.data?.content || res.content || '').replace(/<[^>]*>/g, '').trim() + '\n\n'
      } catch { txt += '（章节内容获取失败）\n\n' }
    }
    const blob = new Blob([txt], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download = `${novelData.title}.txt`; a.click()
    URL.revokeObjectURL(url)
  } catch (err) { console.error('导出失败:', err) }
}

const handleCreateSubmit = async () => {
  if (!createForm.value.title || !createForm.value.genre) return
  creating.value = true
  try {
    const res = await createNovel(createForm.value)
    showCreateDialog.value = false
    createForm.value = { title: '', genre: '', description: '', writing_style: '', core_idea: '' }
    await loadNovels()
    const newId = res.data?.id || res.id
    if (newId) router.push(`/home/novels/${newId}`)
  } catch (err) { console.error('创建失败:', err) } finally { creating.value = false }
}

onMounted(loadNovels)
</script>
