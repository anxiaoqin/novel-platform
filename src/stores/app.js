import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const theme = ref(localStorage.getItem('theme') || 'dark')
  const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

  const setTheme = (newTheme) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  const setUser = (userData) => {
    user.value = userData
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData))
    } else {
      localStorage.removeItem('user')
    }
  }

  // 初始化主题
  document.documentElement.setAttribute('data-theme', theme.value)

  return { theme, user, setTheme, setUser }
})
