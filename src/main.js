import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 样式引入顺序：tailwind → themes → global
import '@/styles/tailwind.css'
import '@/styles/themes.css'
import '@/styles/global.css'

// 主题系统
import { initTheme } from '@/composables/useTheme'

const app = createApp(App)
app.use(createPinia())
app.use(router)

// 初始化主题（必须在mount前调用）
initTheme()

app.mount('#app')
