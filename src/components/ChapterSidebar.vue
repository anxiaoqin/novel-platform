<template>
  <div class="chapter-sidebar" :class="{ collapsed: collapsed }">
    <div class="sidebar-header">
      <button class="collapse-btn" @click="collapsed = !collapsed" :title="collapsed ? '展开' : '收起'">
        <span v-if="collapsed">☰</span>
        <span v-else>⋘</span>
      </button>
      <template v-if="!collapsed">
        <div class="novel-title" @click="goBack" title="返回作品详情">
          <span class="back-arrow">←</span>
          <span class="title-text">{{ novelTitle || '加载中...' }}</span>
        </div>
      </template>
    </div>

    <div class="sidebar-body" v-if="!collapsed">
      <!-- 搜索 -->
      <div class="chapter-search">
        <input v-model="searchQuery" placeholder="搜索章节..." class="search-input" />
      </div>
      <!-- 章节列表 -->
      <div class="chapter-list">
        <div
          v-for="(ch, idx) in filteredChapters"
          :key="ch.id"
          class="chapter-item"
          :class="{ active: ch.id === currentChapterId }"
          @click="$emit('select-chapter', ch)"
        >
          <span class="chapter-order">{{ ch.order || idx + 1 }}</span>
          <span class="chapter-title">{{ ch.title || '无标题' }}</span>
          <span class="chapter-words">{{ getWordCount(ch) }}字</span>
        </div>
        <div v-if="filteredChapters.length === 0" class="empty-hint">
          {{ searchQuery ? '无匹配章节' : '暂无章节' }}
        </div>
      </div>
    </div>

    <!-- 底部新建按钮 -->
    <div class="sidebar-footer" v-if="!collapsed">
      <button class="add-chapter-btn" @click="$emit('add-chapter')">+ 新章节</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  chapters: { type: Array, default: () => [] },
  currentChapterId: { type: [Number, String], default: null },
  novelTitle: { type: String, default: '' },
  collapsed: { type: Boolean, default: false }
})

const emit = defineEmits(['select-chapter', 'add-chapter', 'go-back'])
const searchQuery = ref('')

const filteredChapters = computed(() => {
  if (!searchQuery.value) return props.chapters
  const q = searchQuery.value.toLowerCase()
  return props.chapters.filter(ch => (ch.title || '').toLowerCase().includes(q))
})

const getWordCount = (ch) => {
  if (!ch.content) return 0
  return ch.content.replace(/<[^>]*>/g, '').replace(/\s/g, '').length
}

const goBack = () => emit('go-back')
</script>

<style scoped>
.chapter-sidebar {
  width: 240px;
  min-width: 240px;
  background: var(--sidebar-bg, #16161E);
  border-right: 1px solid var(--border-color, #2A2A36);
  display: flex;
  flex-direction: column;
  transition: width 0.25s, min-width 0.25s;
  overflow: hidden;
  flex-shrink: 0;
}
.chapter-sidebar.collapsed {
  width: 44px;
  min-width: 44px;
}

.sidebar-header {
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid var(--border-color, #2A2A36);
  flex-shrink: 0;
}

.collapse-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: var(--bg-hover, #1E1E28);
  color: var(--text-secondary, #8B8B9E);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.collapse-btn:hover { background: var(--brand-primary-bg, rgba(108,142,239,0.15)); color: var(--brand-primary); }

.novel-title {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary, #E4E4E8);
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.novel-title:hover { color: var(--brand-primary); }
.back-arrow { font-size: 14px; flex-shrink: 0; }
.title-text { overflow: hidden; text-overflow: ellipsis; }

.sidebar-body {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chapter-search {
  padding: 8px 12px;
  flex-shrink: 0;
}
.search-input {
  width: 100%;
  background: var(--bg-input, #1A1A24);
  border: 1px solid var(--border-color, #2A2A36);
  border-radius: 4px;
  padding: 6px 10px;
  color: var(--text-primary, #E4E4E8);
  font-size: 12px;
  outline: none;
  box-sizing: border-box;
}
.search-input:focus { border-color: var(--brand-primary, #6C8EEF); }
.search-input::placeholder { color: var(--text-placeholder, #5A5A6E); }

.chapter-list {
  flex: 1;
  overflow-y: auto;
  padding: 4px 0;
}
.chapter-list::-webkit-scrollbar { width: 4px; }
.chapter-list::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb, #2A2A3A); border-radius: 2px; }

.chapter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 12px;
  color: var(--sidebar-text, #9E9EB2);
  transition: all 0.15s;
  border-left: 3px solid transparent;
}
.chapter-item:hover {
  background: var(--sidebar-hover-bg, rgba(255,255,255,0.04));
  color: var(--text-primary);
}
.chapter-item.active {
  background: var(--sidebar-active-bg, rgba(108,142,239,0.12));
  color: var(--brand-primary);
  border-left-color: var(--sidebar-active-bar, #6C8EEF);
}

.chapter-order {
  width: 20px;
  text-align: right;
  color: var(--text-placeholder, #5A5A6E);
  flex-shrink: 0;
  font-variant-numeric: tabular-nums;
}
.chapter-item.active .chapter-order { color: var(--brand-primary); }

.chapter-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chapter-words {
  font-size: 10px;
  color: var(--text-placeholder, #5A5A6E);
  flex-shrink: 0;
  font-variant-numeric: tabular-nums;
}

.empty-hint {
  padding: 20px 12px;
  text-align: center;
  font-size: 12px;
  color: var(--text-placeholder, #5A5A6E);
}

.sidebar-footer {
  padding: 8px 12px;
  border-top: 1px solid var(--border-color, #2A2A36);
  flex-shrink: 0;
}
.add-chapter-btn {
  width: 100%;
  padding: 6px;
  background: var(--brand-primary-bg, rgba(108,142,239,0.15));
  color: var(--brand-primary, #6C8EEF);
  border: 1px dashed var(--brand-primary, #6C8EEF);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.15s;
}
.add-chapter-btn:hover {
  background: var(--brand-primary-hover, rgba(108,142,239,0.25));
}
</style>
