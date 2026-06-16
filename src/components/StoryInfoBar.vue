<template>
  <div class="story-info-bar">
    <div class="info-left">
      <span class="char-count">{{ charCount }} 字</span>
      <span class="save-indicator" :class="saveStatus">
        <span class="save-dot"></span>{{ saveStatusText }}
      </span>
    </div>
    <div class="info-center">
      <button class="info-btn" @click="openPopup('timeline')" title="时间线">
        <span class="info-icon">⏱</span>
        <span class="info-label">时间线</span>
      </button>
      <button class="info-btn" @click="openPopup('characters')" title="角色卡">
        <span class="info-icon">👤</span>
        <span class="info-label">角色</span>
      </button>
      <button class="info-btn" @click="openPopup('events')" title="事件">
        <span class="info-icon">⚡</span>
        <span class="info-label">事件</span>
      </button>
      <button class="info-btn" @click="openPopup('worlds')" title="世界观">
        <span class="info-icon">🌍</span>
        <span class="info-label">世界观</span>
      </button>
    </div>
    <div class="info-right">
      <div class="theme-switcher">
        <button
          v-for="t in editorThemes" :key="t.value"
          :class="['theme-pip', { active: currentTheme === t.value }]"
          @click="$emit('update:currentTheme', t.value)"
          :title="t.label"
          :style="{ background: t.color }"
        ></button>
      </div>
    </div>

    <!-- 弹窗：时间线 -->
    <Teleport to="body">
      <div v-if="activePopup" class="info-popup-overlay" @click.self="closePopup">
        <div class="info-popup" :class="[`popup-${activePopup}`]">
          <div class="popup-header">
            <h3>{{ popupTitle }}</h3>
            <button class="popup-close" @click="closePopup">✕</button>
          </div>
          <div class="popup-body">
            <!-- 时间线 -->
            <template v-if="activePopup === 'timeline'">
              <div v-if="loading" class="popup-loading">加载中...</div>
              <div v-else-if="popupData.length === 0" class="popup-empty">暂无时间线节点</div>
              <div v-else class="timeline-list">
                <div v-for="item in popupData" :key="item.id" class="timeline-item">
                  <div class="tl-dot" :style="{ background: getEventColor(item.type) }"></div>
                  <div class="tl-content">
                    <div class="tl-title">{{ item.title }}</div>
                    <div class="tl-time" v-if="item.start_time || item.startTime">{{ item.start_time || item.startTime }}</div>
                    <div class="tl-desc" v-if="item.description">{{ item.description }}</div>
                  </div>
                </div>
              </div>
            </template>
            <!-- 角色卡 -->
            <template v-if="activePopup === 'characters'">
              <div v-if="loading" class="popup-loading">加载中...</div>
              <div v-else-if="popupData.length === 0" class="popup-empty">暂无角色</div>
              <div v-else class="character-grid">
                <div v-for="char in popupData" :key="char.id" class="char-card">
                  <div class="char-avatar">{{ (char.name || '?')[0] }}</div>
                  <div class="char-info">
                    <div class="char-name">{{ char.name }}</div>
                    <div class="char-type" v-if="char.type">{{ char.type }}</div>
                    <div class="char-desc" v-if="char.description">{{ char.description.slice(0, 80) }}</div>
                  </div>
                </div>
              </div>
            </template>
            <!-- 事件 -->
            <template v-if="activePopup === 'events'">
              <div v-if="loading" class="popup-loading">加载中...</div>
              <div v-else-if="popupData.length === 0" class="popup-empty">暂无事件</div>
              <div v-else class="event-list">
                <div v-for="evt in popupData" :key="evt.id" class="event-item" :style="{ borderLeftColor: getEventColor(evt.type) }">
                  <div class="evt-header">
                    <span class="evt-type-badge" :style="{ background: getEventColor(evt.type), color: '#fff' }">{{ evt.type || '事件' }}</span>
                    <span class="evt-title">{{ evt.title || evt.name }}</span>
                  </div>
                  <div class="evt-desc" v-if="evt.description">{{ evt.description.slice(0, 120) }}</div>
                </div>
              </div>
            </template>
            <!-- 世界观 -->
            <template v-if="activePopup === 'worlds'">
              <div v-if="loading" class="popup-loading">加载中...</div>
              <div v-else-if="popupData.length === 0" class="popup-empty">暂无世界观设定</div>
              <div v-else class="world-list">
                <div v-for="w in popupData" :key="w.id" class="world-item">
                  <div class="world-type">{{ getWorldIcon(w.type) }} {{ w.type || '设定' }}</div>
                  <div class="world-name">{{ w.name || w.title }}</div>
                  <div class="world-desc" v-if="w.description">{{ w.description.slice(0, 150) }}</div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getTimelines } from '@/api/modules/timeline'
import { getCharacters } from '@/api/modules/character'
import { getWorlds } from '@/api/modules/world'
import api from '@/api'

const props = defineProps({
  charCount: { type: Number, default: 0 },
  saveStatus: { type: String, default: 'saved' },
  novelId: { type: [Number, String], default: null },
  currentTheme: { type: String, default: 'typora' }
})

const emit = defineEmits(['update:currentTheme'])

const editorThemes = [
  { value: 'default', label: '默认', color: '#8B8B9E' },
  { value: 'notion', label: 'Notion风', color: '#FFFFFF' },
  { value: 'typora', label: 'Typora风', color: '#6C8EEF' },
  { value: 'word', label: 'Word风', color: '#2B579A' },
  { value: 'focus', label: '专注模式', color: '#6EE7B7' }
]

const saveStatusText = computed(() => ({
  saved: '已保存', saving: '保存中...', unsaved: '未保存'
}[props.saveStatus] || ''))

const activePopup = ref(null)
const popupData = ref([])
const loading = ref(false)

const popupTitle = computed(() => ({
  timeline: '时间线',
  characters: '角色卡',
  events: '事件列表',
  worlds: '世界观设定'
}[activePopup.value] || ''))

const eventColors = {
  setup: 'var(--color-setup-text, #8AA8F5)',
  conflict: 'var(--color-conflict-text, #EF7A7A)',
  reversal: 'var(--color-reversal-text, #B87AEF)',
  climax: 'var(--color-climax-text, #EFBF5B)',
  success: 'var(--color-success-text, #5BBF8B)',
  transition: 'var(--color-transition-text, #8B8B9E)'
}

const getEventColor = (type) => eventColors[type] || 'var(--brand-primary, #6C8EEF)'

const getWorldIcon = (type) => ({
  region: '🗺', person: '👤', item: '🔮', event: '⚡'
}[type] || '📜')

const openPopup = async (type) => {
  activePopup.value = type
  popupData.value = []
  loading.value = true

  try {
    let res
    switch (type) {
      case 'timeline':
        res = await getTimelines(props.novelId)
        break
      case 'characters':
        res = await getCharacters(props.novelId)
        break
      case 'events':
        res = await api.get(`/novels/${props.novelId}/outline-events`)
        break
      case 'worlds':
        res = await getWorlds(props.novelId)
        break
    }
    popupData.value = res.data?.items || res.data || res || []
  } catch (err) {
    console.error(`加载${popupTitle.value}失败:`, err)
    popupData.value = []
  } finally {
    loading.value = false
  }
}

const closePopup = () => {
  activePopup.value = null
  popupData.value = []
}
</script>

<style scoped>
.story-info-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 12px;
  background: var(--bg-secondary, #16161E);
  border-top: 1px solid var(--border-color, #2A2A36);
  font-size: 11px;
  color: var(--text-secondary, #8B8B9E);
  flex-shrink: 0;
  gap: 8px;
}

.info-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.char-count { font-variant-numeric: tabular-nums; }

.save-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
}
.save-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--status-saved, #6EE7B7);
}
.save-indicator.saving .save-dot {
  background: var(--status-saving, #FDE68A);
  animation: pulse 1s infinite;
}
.save-indicator.unsaved .save-dot { background: var(--status-saving, #FDE68A); }

@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.3; } }

.info-center {
  display: flex;
  align-items: center;
  gap: 2px;
}

.info-btn {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 4px 8px;
  border: none;
  background: transparent;
  color: var(--text-secondary, #8B8B9E);
  border-radius: 4px;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.15s;
  white-space: nowrap;
}
.info-btn:hover {
  background: var(--brand-primary-bg, rgba(108,142,239,0.15));
  color: var(--brand-primary, #6C8EEF);
}

.info-icon { font-size: 13px; }
.info-label { font-size: 11px; }

.info-right {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.theme-switcher {
  display: flex;
  gap: 4px;
  align-items: center;
}

.theme-pip {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--border-color, #2A2A36);
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0.5;
}
.theme-pip:hover { opacity: 0.8; transform: scale(1.15); }
.theme-pip.active { opacity: 1; border-color: var(--brand-primary); transform: scale(1.2); }

/* 弹窗 */
.info-popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: var(--overlay-bg, rgba(0,0,0,0.8));
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-popup {
  width: 520px;
  max-width: 90vw;
  max-height: 70vh;
  background: var(--bg-card, #1A1A24);
  border: 1px solid var(--border-color, #2A2A36);
  border-radius: var(--radius-lg, 12px);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-popover, 0 4px 20px rgba(0,0,0,0.6));
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}
.popup-header h3 {
  margin: 0;
  font-size: 15px;
  color: var(--text-primary);
}
.popup-close {
  width: 28px; height: 28px;
  border: none;
  background: var(--bg-hover);
  color: var(--text-secondary);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}
.popup-close:hover { background: var(--brand-primary-bg); color: var(--brand-primary); }

.popup-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
.popup-body::-webkit-scrollbar { width: 4px; }
.popup-body::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 2px; }

.popup-loading, .popup-empty {
  text-align: center;
  padding: 32px;
  color: var(--text-placeholder);
  font-size: 13px;
}

/* 时间线 */
.timeline-list {
  position: relative;
  padding-left: 16px;
}
.timeline-list::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border-color);
}

.timeline-item {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  position: relative;
}

.tl-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
  position: relative;
  z-index: 1;
}

.tl-content { flex: 1; }
.tl-title { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.tl-time { font-size: 11px; color: var(--text-placeholder); margin-top: 2px; }
.tl-desc { font-size: 12px; color: var(--text-secondary); margin-top: 4px; line-height: 1.6; }

/* 角色卡 */
.character-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.char-card {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: var(--bg-hover);
  border-radius: var(--radius-md, 8px);
  border: 1px solid var(--border-color);
}

.char-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--brand-primary-bg);
  color: var(--brand-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  flex-shrink: 0;
}

.char-info { flex: 1; min-width: 0; }
.char-name { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.char-type { font-size: 11px; color: var(--text-placeholder); margin-top: 2px; }
.char-desc { font-size: 11px; color: var(--text-secondary); margin-top: 4px; line-height: 1.5; }

/* 事件 */
.event-list { display: flex; flex-direction: column; gap: 8px; }
.event-item {
  padding: 10px 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--brand-primary);
}
.evt-header { display: flex; align-items: center; gap: 8px; }
.evt-type-badge {
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-weight: 600;
}
.evt-title { font-size: 13px; color: var(--text-primary); font-weight: 500; }
.evt-desc { font-size: 12px; color: var(--text-secondary); margin-top: 6px; line-height: 1.6; }

/* 世界观 */
.world-list { display: flex; flex-direction: column; gap: 10px; }
.world-item {
  padding: 10px 12px;
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}
.world-type { font-size: 11px; color: var(--text-placeholder); }
.world-name { font-size: 13px; font-weight: 600; color: var(--text-primary); margin-top: 2px; }
.world-desc { font-size: 12px; color: var(--text-secondary); margin-top: 4px; line-height: 1.6; }

/* 移动端 */
@media (max-width: 768px) {
  .info-label { display: none; }
  .info-center { gap: 0; }
  .info-btn { padding: 4px 6px; }
}
</style>
