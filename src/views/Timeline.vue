<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">时间线</h1>
      <Button @click="showCreateDialog = true"><Plus class="mr-2 h-4 w-4" /> 新建事件</Button>
    </div>

    <div class="relative max-w-sm">
      <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <Input v-model="searchQuery" placeholder="搜索事件..." class="pl-9" />
    </div>

    <div v-if="filteredEvents.length" class="relative pl-8">
      <!-- 时间线竖线 -->
      <div class="absolute left-3 top-0 bottom-0 w-0.5 bg-border" />
      <div v-for="event in filteredEvents" :key="event.id" class="relative mb-6">
        <div class="absolute -left-5 top-1.5 h-4 w-4 rounded-full border-2 border-primary bg-background" />
        <Card class="transition-all hover:shadow-sm">
          <CardContent class="pt-4 pb-3">
            <div class="flex items-start justify-between gap-2">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <h3 class="font-semibold text-sm">{{ event.title }}</h3>
                  <Badge v-if="event.event_type" :variant="eventTypeVariant(event.event_type)" class="text-xs">{{ event.event_type }}</Badge>
                </div>
                <p class="mt-1 text-sm text-muted-foreground line-clamp-2">{{ event.description || '暂无描述' }}</p>
                <p v-if="event.timestamp" class="mt-1 text-xs text-muted-foreground">{{ event.timestamp }}</p>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger as-child>
                  <Button variant="ghost" size="icon" class="h-7 w-7 shrink-0"><MoreHorizontal class="h-4 w-4" /></Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem @click="editEvent(event)"><Pencil class="mr-2 h-4 w-4" />编辑</DropdownMenuItem>
                  <DropdownMenuItem @click="deleteEvent(event)" class="text-destructive"><Trash2 class="mr-2 h-4 w-4" />删除</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <div v-else class="flex flex-col items-center py-16 text-muted-foreground">
      <Clock class="h-10 w-10 mb-3" />
      <p>暂无时间线事件，点击创建</p>
    </div>

    <Dialog :open="showCreateDialog" @update:open="showCreateDialog = $event">
      <DialogContent class="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{{ editingEvent ? '编辑事件' : '新建事件' }}</DialogTitle>
        </DialogHeader>
        <form @submit.prevent="saveEvent" class="space-y-4">
          <div class="space-y-2">
            <Label>事件名称 *</Label>
            <Input v-model="eventForm.title" placeholder="事件名称" />
          </div>
          <div class="space-y-2">
            <Label>事件类型</Label>
            <Select v-model="eventForm.event_type">
              <SelectTrigger><SelectValue placeholder="选择类型" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="人物">人物</SelectItem>
                <SelectItem value="环境">环境</SelectItem>
                <SelectItem value="情节">情节</SelectItem>
                <SelectItem value="冲突">冲突</SelectItem>
                <SelectItem value="伏笔">伏笔</SelectItem>
                <SelectItem value="转折">转折</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="space-y-2">
            <Label>描述</Label>
            <Textarea v-model="eventForm.description" placeholder="事件详情" :rows="4" />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" @click="showCreateDialog = false">取消</Button>
            <Button type="submit" :loading="saving">保存</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getTimelines } from '@/api/modules/timeline'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu'
import { Plus, Search, Pencil, Trash2, MoreHorizontal, Clock } from 'lucide-vue-next'

const events = ref([])
const searchQuery = ref('')
const showCreateDialog = ref(false)
const editingEvent = ref(null)
const saving = ref(false)
const eventForm = ref({ title: '', event_type: '', description: '', novel_id: null })

const eventTypeVariant = (type) => {
  const map = { 人物: 'default', 冲突: 'destructive', 转折: 'secondary', 伏笔: 'outline', 情节: 'default', 环境: 'outline' }
  return map[type] || 'outline'
}

const filteredEvents = computed(() => {
  if (!searchQuery.value) return events.value
  const q = searchQuery.value.toLowerCase()
  return events.value.filter(e => e.title?.toLowerCase().includes(q) || e.description?.toLowerCase().includes(q))
})

const loadEvents = async () => { try { const res = await getTimelines(); events.value = res.data?.items || res.data || res || [] } catch {} }
const editEvent = (e) => { editingEvent.value = e; eventForm.value = { title: e.title, event_type: e.event_type || '', description: e.description || '', novel_id: e.novel_id }; showCreateDialog.value = true }
const deleteEvent = async (e) => { if (!confirm(`确定删除事件「${e.title}」？`)) return; try { await deleteEventApi(e.id); loadEvents() } catch {} }
const saveEvent = async () => {
  if (!eventForm.value.title) return
  saving.value = true
  try {
    if (editingEvent.value) await updateTimeline(editingEvent.value.id, eventForm.value)
    else await createTimeline(eventForm.value)
    showCreateDialog.value = false; editingEvent.value = null
    eventForm.value = { title: '', event_type: '', description: '', novel_id: null }
    loadEvents()
  } catch {} finally { saving.value = false }
}

onMounted(loadEvents)
</script>
