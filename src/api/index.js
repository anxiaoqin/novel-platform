import axios from 'axios'

// API基础地址：生产环境用Vercel环境变量，开发环境走Vite代理
const api = axios.create({ 
  baseURL: import.meta.env.VITE_API_URL || '/api/v1', 
  timeout: 30000 
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // 仅在已登录状态下（有token）才清空并跳转，避免登录/注册请求401时误跳转
      const token = localStorage.getItem('token')
      if (token) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        // 避免在登录/注册页反复跳转
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
