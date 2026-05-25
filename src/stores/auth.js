import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
  
  const setToken = (t) => { 
    token.value = t 
    localStorage.setItem('token', t) 
  }
  
  const setUser = (u) => { 
    user.value = u 
    localStorage.setItem('user', JSON.stringify(u)) 
  }
  
  const logout = () => { 
    token.value = '' 
    user.value = {} 
    localStorage.clear() 
  }
  
  return { token, user, setToken, setUser, logout }
})
