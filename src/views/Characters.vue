<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold">角色库</h1>
      <Button @click="showCreateDialog = true"><Plus class="mr-2 h-4 w-4" /> 新建角色</Button>
    </div>

    <!-- Search -->
    <div class="relative max-w-sm">
      <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <Input v-model="searchQuery" placeholder="搜索角色..." class="pl-9" />
    </div>

    <!-- Character Grid -->
    <div v-if="filteredCharacters.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <Card v-for="char in filteredCharacters" :key="char.id" class="transition-all hover:shadow-md">
        <CardContent class="pt-6">
          <div class="flex items-start gap-3">
            <Avatar class="h-12 w-12">
              <AvatarFallback class="bg-primary text-primary-foreground">{{ (char.name || '?').charAt(0) }}</AvatarFallback>
            </Avatar>
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold truncate">{{ char.name }}</h3>
              <p class="text-sm text-muted-foreground line-clamp-2">{{ char.description || '暂无描述' }}</p>
              <div class="mt-2 flex flex-wrap gap-1">
                <Badge v-if="char.role" variant="secondary">{{ char.role }}</Badge>
                <Badge v-if="char.novel_title" variant="outline">{{ char.novel_title }}</Badge>
              </div>
            </div>
          </div>
          <div class="mt-3 flex justify-end gap-1">
            <Button variant="ghost" size="sm" @click="editCharacter(char)"><Pencil class="h-3.5 w-3.5" /></Button>
            <Button variant="ghost" size="sm" class="text-destructive" @click="deleteCharacter(char)"><Trash2 class="h-3.5 w-3.5" /></Button>
          </div>
        </CardContent>
      </Card>
    </div>

    <div v-else class="flex flex-col items-center py-16 text-muted-foreground">
      <Users class="h-10 w-10 mb-3" />
      <p>暂无角色，点击创建</p>
    </div>

    <!-- Create/Edit Dialog -->
    <Dialog :open="showCreateDialog" @update:open="showCreateDialog = $event">
      <DialogContent class="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{{ editingChar ? '编辑角色' : '新建角色' }}</DialogTitle>
        </DialogHeader>
        <form @submit.prevent="saveCharacter" class="space-y-4">
          <div class="space-y-2">
            <Label>角色名称 *</Label>
            <Input v-model="charForm.name" placeholder="请输入角色名称" />
          </div>
          <div class="space-y-2">
            <Label>角色定位</Label>
            <Select v-model="charForm.role">
              <SelectTrigger><SelectValue placeholder="选择角色类型" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="主角">主角</SelectItem>
                <SelectItem value="女主">女主</SelectItem>
                <SelectItem value="配角">配角</SelectItem>
                <SelectItem value="反派">反派</SelectItem>
                <SelectItem value="其他">其他</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="space-y-2">
            <Label>角色描述</Label>
            <Textarea v-model="charForm.description" placeholder="描述角色的性格、背景等" :rows="4" />
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
import { getCharacters, createCharacter } from '@/api/modules/character'
import { getNovels } from '@/api/modules/novel'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Plus, Search, Pencil, Trash2, Users } from 'lucide-vue-next'

const characters = ref([])
const searchQuery = ref('')
const showCreateDialog = ref(false)
const editingChar = ref(null)
const saving = ref(false)

const charForm = ref({ name: '', role: '', description: '', novel_id: null })

const filteredCharacters = computed(() => {
  if (!searchQuery.value) return characters.value
  const q = searchQuery.value.toLowerCase()
  return characters.value.filter(c => c.name?.toLowerCase().includes(q) || c.description?.toLowerCase().includes(q))
})

const loadCharacters = async () => {
  try {
    const res = await getCharacters()
    characters.value = res.data?.items || res.data || res || []
  } catch {}
}

const editCharacter = (char) => {
  editingChar.value = char
  charForm.value = { name: char.name, role: char.role || '', description: char.description || '', novel_id: char.novel_id }
  showCreateDialog.value = true
}

const deleteCharacter = async (char) => {
  if (!confirm(`确定删除角色「${char.name}」吗？`)) return
  try { await deleteCharApi(char.id); loadCharacters() } catch {}
}

const saveCharacter = async () => {
  if (!charForm.value.name) return
  saving.value = true
  try {
    if (editingChar.value) {
      await updateCharacter(editingChar.value.id, charForm.value)
    } else {
      await createCharacter(charForm.value)
    }
    showCreateDialog.value = false
    editingChar.value = null
    charForm.value = { name: '', role: '', description: '', novel_id: null }
    loadCharacters()
  } catch {} finally { saving.value = false }
}

onMounted(loadCharacters)
</script>
