<template>
  <div class="mx-auto max-w-3xl space-y-6 py-8 px-4">
    <h1 class="text-2xl font-bold">法律条款</h1>

    <Tabs v-model="activeTab">
      <TabsList>
        <TabsTrigger value="terms">用户协议</TabsTrigger>
        <TabsTrigger value="privacy">隐私政策</TabsTrigger>
        <TabsTrigger value="ai">AI使用规范</TabsTrigger>
      </TabsList>
      <TabsContent value="terms" class="mt-4">
        <Card>
          <CardContent class="pt-6 prose prose-sm max-w-none text-foreground">
            <h3>一、总则</h3>
            <p>欢迎您使用十方天地AI网文创作平台。请您在使用前仔细阅读本协议。</p>
            <h3>二、账号注册</h3>
            <p>用户需注册账号方可使用平台功能，注册信息应真实有效。</p>
            <h3>三、内容规范</h3>
            <p>用户创作内容应遵守法律法规，不得包含违法违规信息。</p>
          </CardContent>
        </Card>
      </TabsContent>
      <TabsContent value="privacy" class="mt-4">
        <Card>
          <CardContent class="pt-6 prose prose-sm max-w-none text-foreground">
            <h3>隐私保护</h3>
            <p>我们重视用户隐私保护，不会向第三方泄露您的个人信息。</p>
          </CardContent>
        </Card>
      </TabsContent>
      <TabsContent value="ai" class="mt-4">
        <Card>
          <CardContent class="pt-6 prose prose-sm max-w-none text-foreground">
            <h3>AI使用规范</h3>
            <p>AI生成内容仅供参考，用户对最终发布内容负责。AI辅助创作的内容归用户所有。</p>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>

    <div class="flex items-center gap-2">
      <Checkbox :checked="agreed" @update:checked="agreed = $event" />
      <Label class="text-sm">我已阅读并同意以上条款</Label>
    </div>

    <Button :disabled="!agreed" @click="$router.push('/register')">确认并继续</Button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

const activeTab = ref('terms')
const agreed = ref(false)
</script>
