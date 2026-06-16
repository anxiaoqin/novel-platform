/**
 * 十方书社 API 入口文件
 * 基于 axios 的 HTTP 请求封装
 */

import axios from 'axios'
// element-plus removed

// 创建 axios 实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://103.217.187.186:8001/api/v1',
  timeout: 60000, // AI生成可能较慢，超时设为60s
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加 Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 统一处理错误
api.interceptors.response.use(
  (response) => {
    return response.data // 直接返回data，简化调用
  },
  (error) => {
    if (error.response?.status === 401) {
      const token = localStorage.getItem('token')
      if (token) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        console.error('登录已过期，请重新登录')
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api

// 导出所有模块
export * as authApi from './modules/auth'
export * as userApi from './modules/user'
export * as creditsApi from './modules/credits'
export * as novelApi from './modules/novel'
export * as chapterApi from './modules/chapter'
export * as worldApi from './modules/world'
export * as characterApi from './modules/character'
export * as timelineApi from './modules/timeline'
export * as aiApi from './modules/ai'
export * as outlineApi from './modules/outline'
export * as streamApi from './modules/stream'
export * as chapterVersionApi from './modules/chapterVersion'
export * as creationApi from './modules/creation'
export * as publishApi from './modules/publish'
export * as coverApi from './modules/cover'
export * as otherApi from './modules/other'
