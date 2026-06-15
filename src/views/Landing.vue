<template>
  <div class="landing-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-content">
        <div class="nav-brand">
          <span class="brand-icon">📖</span>
          <span class="brand-name">十方天地</span>
        </div>
        <div class="nav-links" v-if="!isMobile">
          <a href="#features">功能</a>
          <a href="#flow">流程</a>
          <a href="#about">关于</a>
        </div>
        <div class="nav-actions">
          <!-- 主题切换 -->
          <div class="theme-switcher">
            <div 
              v-for="t in themes" 
              :key="t.value"
              class="theme-btn"
              :class="{ active: theme === t.value }"
              :title="`${t.label}：${t.desc}`"
              @click="handleThemeChange(t.value)"
            >
              {{ t.icon }}
            </div>
          </div>
          <router-link to="/login">
            <el-button type="primary" size="small">开始创作</el-button>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Hero区域 -->
    <section class="hero">
      <canvas ref="canvasRef" class="particle-canvas"></canvas>
      <div class="hero-content">
        <h1>十方天地，皆有故事</h1>
        <p class="hero-sub">AI辅助网文创作平台 — 人主创，AI辅助</p>
        <div class="hero-actions">
          <router-link to="/register">
            <el-button type="primary" size="large">免费开始</el-button>
          </router-link>
          <router-link to="/login">
            <el-button size="large">登录</el-button>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 功能特性 -->
    <section id="features" class="features">
      <h2>核心功能</h2>
      <div class="feature-grid">
        <div class="feature-card" v-for="f in features" :key="f.title">
          <span class="feature-icon">{{ f.icon }}</span>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- 人机共创流程 -->
    <section id="flow" class="flow-section">
      <h2>人机共创4步流程</h2>
      <p class="flow-sub">人是创作者，AI是辅助者，创作权始终在你手中</p>
      <div class="flow-steps">
        <div class="flow-step" v-for="(step, i) in flowSteps" :key="i">
          <div class="step-number">{{ i + 1 }}</div>
          <div class="step-who">{{ step.who }}</div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.desc }}</p>
        </div>
      </div>
    </section>

    <!-- 底部 -->
    <footer id="about" class="footer">
      <p>© 2026 十方天地 — AI辅助网文创作平台</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useTheme, THEMES } from '@/composables/useTheme'

const { theme, setTheme } = useTheme()
const themes = THEMES

const canvasRef = ref(null)
const windowWidth = ref(window.innerWidth)
const isMobile = computed(() => windowWidth.value < 768)

let animId = null

const handleThemeChange = (newTheme) => {
  setTheme(newTheme)
}

const features = [
  { icon: '🤝', title: '人机共创', desc: '人写灵感、AI分析事件、人选大纲、AI填充正文' },
  { icon: '🔍', title: 'AI纠错', desc: '实时检测文字问题，红色波浪标注，一键修正' },
  { icon: '✨', title: '智能续写', desc: '3个候选续写方案，保持你的风格和节奏' },
  { icon: '🎭', title: '去AI味', desc: '检测AI痕迹，自然改写让文字回归人味' },
  { icon: '📋', title: '角色卡/时间线', desc: '管理角色关系、物品和故事时间线' },
  { icon: '🧬', title: '写作DNA', desc: '提取你的写作风格特征，AI生成自动对齐' },
]

const flowSteps = [
  { who: '人', title: '灵感输入', desc: '自由写作——一段对话、一个场景、一个灵感碎片' },
  { who: 'AI', title: '事件分析', desc: 'AI读取段落，提取3-8个故事事件建议' },
  { who: '人', title: '组合大纲', desc: '挑选事件、拖拽排序、自定义事件，组合你的大纲' },
  { who: 'AI', title: '正文填充', desc: '按你确认的大纲填充正文，保持你的写作风格' },
]

// 粒子动画
const initParticles = () => {
  const canvas = canvasRef.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  const dpr = window.devicePixelRatio || 1

  const resize = () => {
    const rect = canvas.parentElement.getBoundingClientRect()
    canvas.width = rect.width * dpr
    canvas.height = rect.height * dpr
    canvas.style.width = rect.width + 'px'
    canvas.style.height = rect.height + 'px'
    ctx.scale(dpr, dpr)
  }

  resize()
  window.addEventListener('resize', resize)

  const particleCount = isMobile.value ? 30 : 60
  const particles = []

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width / dpr,
      y: Math.random() * canvas.height / dpr,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      r: Math.random() * 2 + 1,
    })
  }

  const getAccentColor = () => {
    // 根据主题选择粒子颜色
    if (theme.value === 'dark') return '91, 139, 250'  // 品牌蓝
    if (theme.value === 'eyecare') return '180, 140, 90'  // 暖棕色
    return '102, 126, 234'  // 默认蓝紫
  }

  const animate = () => {
    const w = canvas.width / dpr
    const h = canvas.height / dpr
    ctx.clearRect(0, 0, w, h)

    const accentColor = getAccentColor()

    particles.forEach(p => {
      p.x += p.vx
      p.y += p.vy
      if (p.x < 0 || p.x > w) p.vx *= -1
      if (p.y < 0 || p.y > h) p.vy *= -1
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(${accentColor}, 0.6)`
      ctx.fill()
    })

    // 连线
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x
        const dy = particles[i].y - particles[j].y
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 120) {
          ctx.beginPath()
          ctx.moveTo(particles[i].x, particles[i].y)
          ctx.lineTo(particles[j].x, particles[j].y)
          ctx.strokeStyle = `rgba(${accentColor}, ${0.2 * (1 - dist / 120)})`
          ctx.lineWidth = 0.5
          ctx.stroke()
        }
      }
    }

    animId = requestAnimationFrame(animate)
  }

  animate()
}

const handleResize = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  initParticles()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (animId) cancelAnimationFrame(animId)
})
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: background 0.3s, color 0.3s;
}

/* 导航栏 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: var(--bg-card);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border-color);
  transition: background 0.3s, border-color 0.3s;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-icon {
  font-size: 24px;
}

.brand-name {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-primary);
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: var(--brand-primary);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 主题切换器 */
.theme-switcher {
  display: flex;
  gap: 4px;
}

.theme-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  background: var(--bg-secondary);
  transition: all 0.2s;
  border: 2px solid transparent;
}

.theme-btn:hover {
  background: var(--bg-hover);
}

.theme-btn.active {
  background: var(--brand-primary-bg);
  border-color: var(--brand-primary);
}

/* Hero */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--brand-primary) 0%, #764ba2 100%);
  overflow: hidden;
  padding: 80px 16px 40px;
}

.particle-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #fff;
  max-width: 600px;
}

.hero-content h1 {
  font-size: 36px;
  margin: 0 0 16px;
  letter-spacing: 2px;
}

.hero-sub {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 32px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 功能特性 */
.features {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 16px;
}

.features h2 {
  text-align: center;
  font-size: 28px;
  margin: 0 0 40px;
  color: var(--text-primary);
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.feature-card {
  padding: 24px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  transition: transform 0.2s, box-shadow 0.2s;
  background: var(--bg-card);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
  border-color: var(--brand-primary);
}

.feature-icon {
  font-size: 32px;
  display: block;
  margin-bottom: 12px;
}

.feature-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
  color: var(--text-primary);
}

.feature-card p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

/* 人机共创流程 */
.flow-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 16px;
}

.flow-section h2 {
  text-align: center;
  font-size: 28px;
  margin: 0 0 8px;
  color: var(--text-primary);
}

.flow-sub {
  text-align: center;
  color: var(--text-secondary);
  margin: 0 0 40px;
}

.flow-steps {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.flow-step {
  text-align: center;
  padding: 24px 16px;
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--brand-primary);
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.step-who {
  font-size: 12px;
  color: var(--brand-primary);
  font-weight: bold;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.flow-step h3 {
  margin: 0 0 8px;
  font-size: 16px;
  color: var(--text-primary);
}

.flow-step p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

/* 底部 */
.footer {
  text-align: center;
  padding: 24px 16px;
  color: var(--text-secondary);
  font-size: 13px;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

/* 移动端适配 */
@media (max-width: 767px) {
  .hero-content h1 {
    font-size: 24px;
  }

  .hero-sub {
    font-size: 14px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .hero-actions .el-button {
    width: 100%;
    max-width: 240px;
  }

  .features h2,
  .flow-section h2 {
    font-size: 22px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .flow-steps {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .flow-step {
    padding: 16px 8px;
  }

  .step-number {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }

  .flow-step h3 {
    font-size: 14px;
  }

  .nav-content {
    padding: 0 12px;
    height: 48px;
  }

  .brand-name {
    font-size: 15px;
  }

  .brand-icon {
    font-size: 20px;
  }
}

@media (max-width: 380px) {
  .flow-steps {
    grid-template-columns: 1fr;
  }
}
</style>
