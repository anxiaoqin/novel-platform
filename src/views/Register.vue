<template>
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-br from-primary/20 via-background to-primary/5 p-4">
    <Card class="w-full max-w-sm">
      <CardHeader class="text-center">
        <div class="mx-auto mb-2 text-4xl">📖</div>
        <CardTitle class="text-xl">创建账号</CardTitle>
        <CardDescription>加入十方天地，开始创作</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="space-y-2">
            <Label for="username">用户名</Label>
            <Input id="username" v-model="form.username" placeholder="请输入用户名" />
          </div>
          <div class="space-y-2">
            <Label for="email">邮箱</Label>
            <Input id="email" v-model="form.email" type="email" placeholder="请输入邮箱" />
          </div>
          <div class="space-y-2">
            <Label for="password">密码</Label>
            <Input id="password" v-model="form.password" type="password" placeholder="至少6位" />
          </div>
          <Button type="submit" class="w-full" :loading="loading">注册</Button>
        </form>
      </CardContent>
      <CardFooter class="justify-center">
        <span class="text-sm text-muted-foreground">已有账号？</span>
        <router-link to="/login" class="text-sm text-primary hover:underline ml-1">立即登录</router-link>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'

const router = useRouter()
const loading = ref(false)

const form = reactive({ username: '', email: '', password: '' })

const handleRegister = async () => {
  if (!form.username || !form.email || !form.password) return
  loading.value = true
  try {
    await api.post('/auth/register', { ...form, agreements_accepted: true })
    router.push('/login')
  } catch (err) {
    const msg = err.response?.data?.error || err.response?.data?.detail || err.message || '注册失败'
    alert(msg)
  } finally {
    loading.value = false
  }
}
</script>
