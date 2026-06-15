/**
 * 主题切换 composable
 * 提供三套主题切换能力：暗色（默认）、浅色、纸感护眼模式
 */
import { ref, watch, onMounted } from 'vue'

const THEME_KEY = 'sf-theme'

// 可用主题列表
export const THEMES = [
  { value: 'dark', label: '暗色', icon: '🌙', desc: '深空灰 · 沉浸创作' },
  { value: 'light', label: '浅色', icon: '☀️', desc: '明亮清爽 · 传统风格' },
  { value: 'eyecare', label: '护眼', icon: '📖', desc: '暖米色 · 纸质感' }
]

// 获取初始主题（优先从 localStorage 读取，否则默认暗色）
const getInitialTheme = () => {
  if (typeof window === 'undefined') return 'dark'
  return localStorage.getItem(THEME_KEY) || 'dark'
}

// 当前主题
const currentTheme = ref(getInitialTheme())

// 监听器列表
const listeners = new Set()

/**
 * 设置主题
 * @param {string} theme - 主题值：'dark' | 'light' | 'eyecare'
 */
export function setTheme(theme) {
  if (!THEMES.find(t => t.value === theme)) {
    console.warn(`[useTheme] Unknown theme: ${theme}`)
    return
  }
  
  currentTheme.value = theme
  localStorage.setItem(THEME_KEY, theme)
  
  // 设置 document 属性
  if (typeof document !== 'undefined') {
    document.documentElement.setAttribute('data-theme', theme)
  }
  
  // 通知所有监听器
  listeners.forEach(fn => fn(theme))
}

/**
 * 获取当前主题
 */
export function getTheme() {
  return currentTheme.value
}

/**
 * 获取主题信息
 */
export function getThemeInfo(theme) {
  return THEMES.find(t => t.value === theme) || THEMES[0]
}

/**
 * 初始化主题（应用保存的主题或默认主题）
 */
export function initTheme() {
  if (typeof document !== 'undefined' && !document.documentElement.getAttribute('data-theme')) {
    setTheme(currentTheme.value)
  }
}

/**
 * 切换到下一个主题
 */
export function toggleTheme() {
  const currentIndex = THEMES.findIndex(t => t.value === currentTheme.value)
  const nextIndex = (currentIndex + 1) % THEMES.length
  setTheme(THEMES[nextIndex].value)
}

/**
 * 监听主题变化
 */
export function onThemeChange(callback) {
  listeners.add(callback)
  return () => listeners.delete(callback)
}

/**
 * useTheme hook
 * 在组件中使用
 */
export function useTheme() {
  // 组件挂载时初始化
  onMounted(() => {
    initTheme()
  })
  
  // 监听主题变化
  watch(currentTheme, (newTheme) => {
    setTheme(newTheme)
  }, { immediate: false })
  
  return {
    // 当前主题
    theme: currentTheme,
    themeInfo: () => getThemeInfo(currentTheme.value),
    
    // 可用主题列表
    themes: THEMES,
    
    // 方法
    setTheme,
    toggleTheme,
    getTheme,
    getThemeInfo,
    
    // 便捷属性
    isDark: () => currentTheme.value === 'dark',
    isLight: () => currentTheme.value === 'light',
    isEyecare: () => currentTheme.value === 'eyecare'
  }
}

export default useTheme
