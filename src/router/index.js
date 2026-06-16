import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Landing', component: () => import('@/views/Landing.vue') },
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') },
  {
    path: '/home',
    component: () => import('@/components/layout/AppLayout.vue'),
    children: [
      { path: '', redirect: '/home/novels' },
      { path: 'novels', name: 'Novels', component: () => import('@/views/Novels.vue') },
      { path: 'novels/:id', name: 'NovelDetail', component: () => import('@/views/NovelDetail.vue') },
      { path: 'worlds', name: 'Worlds', component: () => import('@/views/Worlds.vue') },
      { path: 'characters', name: 'Characters', component: () => import('@/views/Characters.vue') },
      { path: 'timeline', name: 'Timeline', component: () => import('@/views/Timeline.vue') },
      { path: 'ai-write', name: 'AIWrite', component: () => import('@/views/AIWrite.vue') },
      { path: 'co-creation', name: 'CoCreation', component: () => import('@/views/CoCreation.vue') },
      { path: 'writing-dna', name: 'WritingDNA', component: () => import('@/views/WritingDNA.vue') },
      { path: 'publish', name: 'Publish', component: () => import('@/views/Publish.vue') },
      { path: 'settings', name: 'Settings', component: () => import('@/views/Settings.vue') }
    ]
  },
  { path: '/write/:novelId/:chapterId', name: 'WritingWorkspace', component: () => import('@/views/WritingWorkspace.vue') },
  { path: '/agreements', name: 'Agreements', component: () => import('@/views/Agreements.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (!token && to.path !== '/' && to.path !== '/login' && to.path !== '/register' && to.path !== '/agreements') {
    next('/login')
  } else {
    next()
  }
})

export default router
