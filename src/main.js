import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router'

// 主题系统
import '@/styles/themes.css'
import '@/styles/global.css'
import { initTheme } from '@/composables/useTheme'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

// 初始化主题（必须在mount前调用）
initTheme()

app.mount('#app')
