<template>
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-br from-primary/20 via-background to-primary/5 p-4">
    <Card class="w-full max-w-sm">
      <CardHeader class="text-center">
        <div class="mx-auto mb-2 text-4xl">📖</div>
        <CardTitle class="text-xl">十方天地</CardTitle>
        <CardDescription>AI辅助网文创作平台</CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="space-y-2">
            <Label for="username">用户名</Label>
            <Input id="username" v-model="form.username" placeholder="请输入用户名" />
          </div>
          <div class="space-y-2">
            <Label for="password">密码</Label>
            <Input id="password" v-model="form.password" type="password" placeholder="请输入密码" @keyup.enter="handleLogin" />
          </div>
          <Button type="submit" class="w-full" :loading="loading">登录</Button>
        </form>
      </CardContent>
      <CardFooter class="justify-center">
        <span class="text-sm text-muted-foreground">还没有账号？</span>
        <router-link to="/register" class="text-sm text-primary hover:underline ml-1">免费注册</router-link>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)

const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.username || !form.password) return
  loading.value = true
  try {
    const res = await api.post('/auth/login', form)
    authStore.setToken(res.token)
    authStore.setUser(res.user)
    router.push('/home')
  } catch (err) {
    const msg = err.response?.data?.error || err.response?.data?.detail || err.message || '登录失败'
    alert(msg)
  } finally {
    loading.value = false
  }
}
</script>
