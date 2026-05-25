import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') },
  { 
    path: '/home', 
    name: 'Home', 
    component: () => import('@/views/Home.vue'),
    children: [
      { path: '', redirect: '/home/novels' },
      { path: 'novels', name: 'Novels', component: () => import('@/views/Novels.vue') },
      { path: 'novels/:id', name: 'NovelDetail', component: () => import('@/views/NovelDetail.vue') },
      { path: 'worlds', name: 'Worlds', component: () => import('@/views/Worlds.vue') },
      { path: 'characters', name: 'Characters', component: () => import('@/views/Characters.vue') },
      { path: 'ai-write', name: 'AIWrite', component: () => import('@/views/AIWrite.vue') },
      { path: 'publish', name: 'Publish', component: () => import('@/views/Publish.vue') },
      { path: 'settings', name: 'Settings', component: () => import('@/views/Settings.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (!token && to.path !== '/login' && to.path !== '/register') {
    next('/login')
  } else {
    next()
  }
})

export default router
