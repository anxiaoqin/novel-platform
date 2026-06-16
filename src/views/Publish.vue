<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold">多平台发布</h1>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <Card v-for="platform in platforms" :key="platform.id" class="transition-all hover:shadow-md">
        <CardContent class="pt-6 text-center">
          <span class="text-4xl">{{ platform.icon }}</span>
          <h3 class="mt-3 font-semibold">{{ platform.name }}</h3>
          <p class="mt-1 text-sm text-muted-foreground">{{ platform.desc }}</p>
          <Badge variant="outline" class="mt-2">{{ platform.status }}</Badge>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const platforms = [
  { id: 1, icon: '📱', name: '起点中文网', desc: '国内最大网文平台', status: '即将支持' },
  { id: 2, icon: '📚', name: '番茄小说', desc: '免费阅读平台', status: '即将支持' },
  { id: 3, icon: '🌐', name: '知乎盐选', desc: '短篇付费阅读', status: '即将支持' },
]
</script>
