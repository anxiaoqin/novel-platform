<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- 导航栏 -->
    <nav class="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
      <div class="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
        <div class="flex items-center gap-2">
          <span class="text-2xl">📖</span>
          <span class="text-lg font-bold">十方天地</span>
        </div>
        <div class="hidden md:flex items-center gap-6 text-sm text-muted-foreground">
          <a href="#features" class="hover:text-foreground transition-colors">功能</a>
          <a href="#flow" class="hover:text-foreground transition-colors">流程</a>
          <a href="#about" class="hover:text-foreground transition-colors">关于</a>
        </div>
        <div class="flex items-center gap-2">
          <!-- 主题切换 -->
          <div class="flex gap-1">
            <button
              v-for="t in themes"
              :key="t.value"
              class="flex h-8 w-8 items-center justify-center rounded-md text-sm transition-colors hover:bg-accent"
              :class="{ 'bg-accent text-accent-foreground': currentTheme === t.value }"
              :title="t.label"
              @click="handleThemeChange(t.value)"
            >{{ t.icon }}</button>
          </div>
          <Separator orientation="vertical" class="h-6" />
          <router-link to="/login">
            <Button variant="ghost" size="sm">登录</Button>
          </router-link>
          <router-link to="/register">
            <Button size="sm">免费开始</Button>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="relative overflow-hidden py-20 md:py-32">
      <div class="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-primary/5" />
      <div class="relative mx-auto max-w-4xl px-4 text-center">
        <Badge variant="secondary" class="mb-4">AI驱动 · 全流程创作</Badge>
        <h1 class="text-4xl md:text-6xl font-bold tracking-tight">
          从灵感到作品<br>
          <span class="bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent">AI陪你走完每一步</span>
        </h1>
        <p class="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
          人机共创4步流程，6步完成100+章长文稳定输出。AI是辅助者，创作权始终在你手中。
        </p>
        <div class="mt-8 flex justify-center gap-3">
          <router-link to="/register">
            <Button size="lg">开始创作新小说</Button>
          </router-link>
          <router-link to="/login">
            <Button variant="outline" size="lg">浏览作品</Button>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section id="features" class="mx-auto max-w-6xl px-4 py-16">
      <h2 class="text-center text-3xl font-bold">核心功能</h2>
      <p class="mt-2 text-center text-muted-foreground">六大AI能力，覆盖网文创作全流程</p>
      <div class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card v-for="f in features" :key="f.title" class="transition-all hover:shadow-md hover:-translate-y-0.5">
          <CardHeader>
            <span class="text-3xl">{{ f.icon }}</span>
            <CardTitle class="text-base">{{ f.title }}</CardTitle>
          </CardHeader>
          <CardContent>
            <p class="text-sm text-muted-foreground">{{ f.desc }}</p>
          </CardContent>
        </Card>
      </div>
    </section>

    <!-- Flow -->
    <section id="flow" class="mx-auto max-w-6xl px-4 py-16">
      <h2 class="text-center text-3xl font-bold">人机共创4步流程</h2>
      <p class="mt-2 text-center text-muted-foreground">人是创作者，AI是辅助者</p>
      <div class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div v-for="(step, i) in flowSteps" :key="i" class="relative rounded-lg border border-border bg-card p-6 text-center">
          <div class="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">{{ i + 1 }}</div>
          <Badge variant="outline" class="mt-3 text-xs">{{ step.who }}</Badge>
          <h3 class="mt-2 font-semibold">{{ step.title }}</h3>
          <p class="mt-1 text-sm text-muted-foreground">{{ step.desc }}</p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="mx-auto max-w-4xl px-4 py-20 text-center">
      <h2 class="text-3xl font-bold">准备好开始创作了吗？</h2>
      <p class="mt-3 text-muted-foreground">免费注册，立刻体验AI辅助创作</p>
      <router-link to="/register">
        <Button size="lg" class="mt-6">立即开始创作</Button>
      </router-link>
    </section>

    <!-- Footer -->
    <footer id="about" class="border-t border-border bg-secondary/50 py-6 text-center text-sm text-muted-foreground">
      © 2026 十方天地 — AI辅助网文创作平台
    </footer>
  </div>
</template>

<script setup>
import { useTheme, THEMES } from '@/composables/useTheme'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'

const { theme: currentTheme, setTheme } = useTheme()
const themes = THEMES

const handleThemeChange = (t) => setTheme(t)

const features = [
  { icon: '🤝', title: '人机共创', desc: '人写灵感、AI分析事件、人选大纲、AI填充正文' },
  { icon: '🔍', title: 'AI纠错', desc: '实时检测文字问题，红色波浪标注，一键修正' },
  { icon: '✨', title: '智能续写', desc: '3个候选续写方案，保持你的风格和节奏' },
  { icon: '🎭', title: '去AI味', desc: '检测AI痕迹，自然改写让文字回归人味' },
  { icon: '📋', title: '角色卡/时间线', desc: '管理角色关系、物品和故事时间线' },
  { icon: '🧬', title: '写作DNA', desc: '提取你的写作风格特征，AI生成自动对齐' },
]

const flowSteps = [
  { who: '人', title: '灵感输入', desc: '自由写作——一段对话、一个场景、一个灵感碎片' },
  { who: 'AI', title: '事件分析', desc: 'AI读取段落，提取3-8个故事事件建议' },
  { who: '人', title: '组合大纲', desc: '挑选事件、拖拽排序、自定义事件，组合你的大纲' },
  { who: 'AI', title: '正文填充', desc: '按你确认的大纲填充正文，保持你的写作风格' },
]
</script>
