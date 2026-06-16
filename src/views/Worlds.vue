<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">世界观设定</h1>
      <Button @click="showCreateDialog = true"><Plus class="mr-2 h-4 w-4" /> 新建设定</Button>
    </div>

    <div class="relative max-w-sm">
      <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <Input v-model="searchQuery" placeholder="搜索世界观..." class="pl-9" />
    </div>

    <div v-if="filteredWorlds.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <Card v-for="world in filteredWorlds" :key="world.id" class="transition-all hover:shadow-md group">
        <CardHeader>
          <div class="flex items-start justify-between">
            <CardTitle class="text-base">{{ world.name }}</CardTitle>
            <DropdownMenu>
              <DropdownMenuTrigger as-child>
                <Button variant="ghost" size="icon" class="h-7 w-7 opacity-0 group-hover:opacity-100"><MoreHorizontal class="h-4 w-4" /></Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem @click="editWorld(world)"><Pencil class="mr-2 h-4 w-4" />编辑</DropdownMenuItem>
                <DropdownMenuItem @click="deleteWorld(world)" class="text-destructive"><Trash2 class="mr-2 h-4 w-4" />删除</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground line-clamp-3">{{ world.description || '暂无描述' }}</p>
          <div class="mt-2 flex flex-wrap gap-1">
            <Badge v-if="world.category" variant="outline">{{ world.category }}</Badge>
          </div>
        </CardContent>
      </Card>
    </div>

    <div v-else class="flex flex-col items-center py-16 text-muted-foreground">
      <Globe class="h-10 w-10 mb-3" />
      <p>暂无世界观设定，点击创建</p>
    </div>

    <Dialog :open="showCreateDialog" @update:open="showCreateDialog = $event">
      <DialogContent class="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{{ editingWorld ? '编辑世界观' : '新建世界观' }}</DialogTitle>
        </DialogHeader>
        <form @submit.prevent="saveWorld" class="space-y-4">
          <div class="space-y-2">
            <Label>名称 *</Label>
            <Input v-model="worldForm.name" placeholder="世界观名称" />
          </div>
          <div class="space-y-2">
            <Label>分类</Label>
            <Input v-model="worldForm.category" placeholder="如：地理、历史、魔法体系" />
          </div>
          <div class="space-y-2">
            <Label>描述</Label>
            <Textarea v-model="worldForm.description" placeholder="详细描述" :rows="5" />
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
import { getWorlds } from '@/api/modules/world'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu'
import { Plus, Search, Pencil, Trash2, MoreHorizontal, Globe } from 'lucide-vue-next'

const worlds = ref([])
const searchQuery = ref('')
const showCreateDialog = ref(false)
const editingWorld = ref(null)
const saving = ref(false)
const worldForm = ref({ name: '', category: '', description: '', novel_id: null })

const filteredWorlds = computed(() => {
  if (!searchQuery.value) return worlds.value
  const q = searchQuery.value.toLowerCase()
  return worlds.value.filter(w => w.name?.toLowerCase().includes(q) || w.description?.toLowerCase().includes(q))
})

const loadWorlds = async () => { try { const res = await getWorlds(); worlds.value = res.data?.items || res.data || res || [] } catch {} }
const editWorld = (w) => { editingWorld.value = w; worldForm.value = { name: w.name, category: w.category || '', description: w.description || '', novel_id: w.novel_id }; showCreateDialog.value = true }
const deleteWorld = async (w) => { if (!confirm(`确定删除「${w.name}」？`)) return; try { await deleteWorldApi(w.id); loadWorlds() } catch {} }
const saveWorld = async () => {
  if (!worldForm.value.name) return
  saving.value = true
  try {
    if (editingWorld.value) await updateWorld(editingWorld.value.id, worldForm.value)
    else await createWorld(worldForm.value)
    showCreateDialog.value = false; editingWorld.value = null
    worldForm.value = { name: '', category: '', description: '', novel_id: null }
    loadWorlds()
  } catch {} finally { saving.value = false }
}

onMounted(loadWorlds)
</script>
