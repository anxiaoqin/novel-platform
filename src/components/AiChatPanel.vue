<template>
  <div class="ai-chat-panel" :class="{ collapsed: collapsed }">
    <!-- 头部 -->
    <div class="chat-header">
      <template v-if="!collapsed">
        <div class="header-left">
          <span class="ai-indicator" :class="{ working: isStreaming }"></span>
          <span class="header-title">AI 助手</span>
        </div>
        <div class="header-actions">
          <button class="clear-btn" @click="clearMessages" title="清空对话">🗑</button>
          <button class="collapse-btn" @click="$emit('update:collapsed', true)" title="收起">⋙</button>
        </div>
      </template>
      <template v-else>
        <button class="expand-btn" @click="$emit('update:collapsed', false)" title="展开AI助手">AI</button>
      </template>
    </div>

    <template v-if="!collapsed">
      <!-- 快捷操作 -->
      <div class="quick-actions">
        <button
          v-for="action in quickActions"
          :key="action.key"
          class="action-chip"
          :class="{ active: activeAction === action.key }"
          @click="handleQuickAction(action.key)"
          :disabled="isStreaming"
        >
          <span class="chip-icon">{{ action.icon }}</span>
          <span class="chip-label">{{ action.label }}</span>
        </button>
      </div>

      <!-- 消息列表 -->
      <div class="chat-messages" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-hint">
          <p>💡 选中文字后可快速调用AI</p>
          <p>或使用上方快捷按钮</p>
        </div>
        <div
          v-for="(msg, idx) in messages"
          :key="idx"
          class="chat-msg"
          :class="msg.role"
        >
          <div class="msg-avatar">{{ msg.role === 'user' ? '✍' : '🤖' }}</div>
          <div class="msg-body">
            <div class="msg-text" v-html="renderMarkdown(msg.content)"></div>
            <div v-if="msg.role === 'assistant' && msg.content && !isStreaming" class="msg-actions">
              <button class="msg-action-btn" @click="insertToEditor(msg.content)" title="插入到编辑器">📝 插入</button>
              <button class="msg-action-btn" @click="replaceSelection(msg.content)" title="替换选中文字">🔄 替换</button>
            </div>
          </div>
        </div>
        <div v-if="isStreaming" class="chat-msg assistant streaming">
          <div class="msg-avatar">🤖</div>
          <div class="msg-body">
            <div class="msg-text streaming-text">{{ streamingContent }}<span class="cursor-blink">|</span></div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="chat-input-area">
        <div class="input-wrapper">
          <textarea
            v-model="inputText"
            @keydown.enter.exact="sendByEnter"
            placeholder="输入指令或问题..."
            class="chat-input"
            rows="1"
            :disabled="isStreaming"
          ></textarea>
          <button class="send-btn" @click="sendMessage" :disabled="!inputText.trim() || isStreaming">
            {{ isStreaming ? '⏳' : '➤' }}
          </button>
        </div>
        <div class="input-hint">Enter 发送 · Shift+Enter 换行</div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { createSSEStream, extractContent } from '@/api/sse'

const props = defineProps({
  collapsed: { type: Boolean, default: false },
  novelId: { type: [Number, String], default: null },
  chapterId: { type: [Number, String], default: null },
  selectedText: { type: String, default: '' },
  editorContent: { type: String, default: '' }
})

const emit = defineEmits(['update:collapsed', 'insert-to-editor', 'replace-selection'])

const messages = ref([])
const inputText = ref('')
const isStreaming = ref(false)
const streamingContent = ref('')
const activeAction = ref(null)
const messagesContainer = ref(null)
let streamController = null

const quickActions = [
  { key: 'continue', icon: '✨', label: '续写', endpoint: '/ai/continue-writing/stream' },
  { key: 'polish', icon: '🎨', label: '润色', endpoint: '/ai/deai-rewrite/stream' },
  { key: 'proofread', icon: '🔍', label: '纠错', endpoint: '/ai/proofread/stream' },
  { key: 'inspire', icon: '💡', label: '灵感', endpoint: '/ai/analyze-paragraph/stream' },
  { key: 'search', icon: '📚', label: '查资料', endpoint: '/ai/knowledge-search/stream' }
]

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

watch(() => messages.value.length, scrollToBottom)
watch(streamingContent, scrollToBottom)

const renderMarkdown = (text) => {
  if (!text) return ''
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
}

const handleQuickAction = (key) => {
  const action = quickActions.find(a => a.key === key)
  if (!action) return

  activeAction.value = key

  let body = {}
  const selected = props.selectedText
  const content = props.editorContent

  switch (key) {
    case 'continue':
      body = { chapterId: props.chapterId, content }
      messages.value.push({ role: 'user', content: '✨ 继续续写...' })
      break
    case 'polish':
      body = { text: selected || content?.slice(-500) || '', style: '网文风格' }
      messages.value.push({ role: 'user', content: `🎨 润色以下内容：\n${(selected || '当前段落').slice(0, 100)}...` })
      break
    case 'proofread':
      body = { content: selected || content?.slice(-1000) || '' }
      messages.value.push({ role: 'user', content: '🔍 纠错检查' })
      break
    case 'inspire':
      body = { content: selected || content?.slice(-500) || '', novelId: props.novelId, chapterId: props.chapterId }
      messages.value.push({ role: 'user', content: '💡 提供灵感和建议' })
      break
    case 'search':
      body = { query: selected || inputText.value || '' }
      messages.value.push({ role: 'user', content: `📚 查资料：${selected || inputText.value || '当前内容相关'}` })
      break
  }

  streamRequest(action.endpoint, body)
}

const sendMessage = () => {
  const text = inputText.value.trim()
  if (!text || isStreaming.value) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''

  // 默认走chat接口
  streamRequest('/ai/chat/stream', {
    message: text,
    novelId: props.novelId,
    chapterId: props.chapterId,
    context: props.selectedText || props.editorContent?.slice(-500) || ''
  })
}

const sendByEnter = (e) => {
  if (e.shiftKey) return
  e.preventDefault()
  sendMessage()
}

const streamRequest = (url, body) => {
  isStreaming.value = true
  streamingContent.value = ''
  activeAction.value = null

  const token = localStorage.getItem('token')
  const baseUrl = localStorage.getItem('apiBase') || ''

  // 动态import获取baseURL
  import('@/api/index.js').then(apiModule => {
    const fetchUrl = `${apiModule.default.defaults.baseURL}${url}`

    streamController = createSSEStream(url, body, {
      onMessage: (data) => {
        const content = extractContent(data)
        if (content) {
          streamingContent.value += content
        }
      },
      onDone: () => {
        if (streamingContent.value) {
          messages.value.push({ role: 'assistant', content: streamingContent.value })
        }
        streamingContent.value = ''
        isStreaming.value = false
        streamController = null
      },
      onError: (err) => {
        streamingContent.value = ''
        messages.value.push({ role: 'assistant', content: '⚠️ 请求失败，请稍后重试' })
        isStreaming.value = false
        streamController = null
      }
    })
  })
}

const stopStream = () => {
  if (streamController) {
    streamController.abort()
    streamController = null
  }
  if (streamingContent.value) {
    messages.value.push({ role: 'assistant', content: streamingContent.value })
  }
  streamingContent.value = ''
  isStreaming.value = false
}

const clearMessages = () => {
  messages.value = []
  streamingContent.value = ''
}

const insertToEditor = (content) => emit('insert-to-editor', content)
const replaceSelection = (content) => emit('replace-selection', content)

defineExpose({ stopStream, clearMessages })
</script>

<style scoped>
.ai-chat-panel {
  width: 320px;
  min-width: 320px;
  background: var(--sidebar-bg, #16161E);
  border-left: 1px solid var(--border-color, #2A2A36);
  display: flex;
  flex-direction: column;
  transition: width 0.25s, min-width 0.25s;
  overflow: hidden;
  flex-shrink: 0;
}
.ai-chat-panel.collapsed {
  width: 44px;
  min-width: 44px;
}

/* 头部 */
.chat-header {
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color, #2A2A36);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--status-saved, #6EE7B7);
  flex-shrink: 0;
}
.ai-indicator.working {
  background: var(--status-ai-working, #C4B5FD);
  animation: pulse 1s infinite;
}

@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.3; } }

.header-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary, #E4E4E8);
}

.header-actions {
  display: flex;
  gap: 4px;
}

.clear-btn, .collapse-btn, .expand-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: var(--bg-hover, #1E1E28);
  color: var(--text-secondary, #8B8B9E);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.clear-btn:hover, .collapse-btn:hover, .expand-btn:hover {
  background: var(--brand-primary-bg, rgba(108,142,239,0.15));
  color: var(--brand-primary);
}

.expand-btn {
  width: auto;
  padding: 0 8px;
  font-weight: 600;
  font-size: 11px;
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  gap: 4px;
  padding: 8px 12px;
  flex-wrap: wrap;
  border-bottom: 1px solid var(--border-color, #2A2A36);
  flex-shrink: 0;
}

.action-chip {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 4px 8px;
  border: 1px solid var(--border-color, #2A2A36);
  border-radius: 12px;
  background: transparent;
  color: var(--text-secondary, #8B8B9E);
  cursor: pointer;
  font-size: 11px;
  transition: all 0.15s;
  white-space: nowrap;
}
.action-chip:hover {
  border-color: var(--brand-primary, #6C8EEF);
  color: var(--brand-primary);
  background: var(--brand-primary-bg, rgba(108,142,239,0.08));
}
.action-chip.active {
  border-color: var(--brand-primary);
  background: var(--brand-primary-bg);
  color: var(--brand-primary);
}
.action-chip:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.chip-icon { font-size: 12px; }
.chip-label { font-size: 11px; }

/* 消息列表 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}
.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb, #2A2A3A); border-radius: 2px; }

.welcome-hint {
  text-align: center;
  color: var(--text-placeholder, #5A5A6E);
  font-size: 12px;
  padding: 32px 12px;
  line-height: 2;
}

.chat-msg {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  align-items: flex-start;
}

.msg-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  flex-shrink: 0;
  background: var(--bg-hover, #1E1E28);
}

.msg-body {
  flex: 1;
  min-width: 0;
}

.msg-text {
  font-size: 12px;
  line-height: 1.7;
  color: var(--text-primary, #E4E4E8);
  word-break: break-word;
}

.chat-msg.user .msg-text {
  color: var(--brand-primary-light, #8AA8F5);
}

.chat-msg.user .msg-avatar {
  background: var(--brand-primary-bg, rgba(108,142,239,0.15));
}

.streaming-text {
  color: var(--ai-text-generated, #C4B5FD);
}

.cursor-blink {
  animation: blink 0.8s infinite;
  color: var(--brand-primary, #6C8EEF);
}
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0; } }

/* 消息操作 */
.msg-actions {
  display: flex;
  gap: 6px;
  margin-top: 6px;
}

.msg-action-btn {
  padding: 2px 8px;
  border: 1px solid var(--border-color, #2A2A36);
  border-radius: 4px;
  background: transparent;
  color: var(--text-secondary, #8B8B9E);
  cursor: pointer;
  font-size: 10px;
  transition: all 0.15s;
}
.msg-action-btn:hover {
  border-color: var(--brand-primary);
  color: var(--brand-primary);
  background: var(--brand-primary-bg);
}

/* 输入区 */
.chat-input-area {
  padding: 8px 12px 12px;
  border-top: 1px solid var(--border-color, #2A2A36);
  flex-shrink: 0;
}

.input-wrapper {
  display: flex;
  gap: 6px;
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  background: var(--bg-input, #1A1A24);
  border: 1px solid var(--border-color, #2A2A36);
  border-radius: 6px;
  padding: 8px 10px;
  color: var(--text-primary, #E4E4E8);
  font-size: 12px;
  line-height: 1.5;
  outline: none;
  resize: none;
  max-height: 100px;
  font-family: inherit;
}
.chat-input:focus { border-color: var(--brand-primary, #6C8EEF); }
.chat-input::placeholder { color: var(--text-placeholder, #5A5A6E); }

.send-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: var(--brand-primary, #6C8EEF);
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: opacity 0.15s;
}
.send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.send-btn:not(:disabled):hover { opacity: 0.85; }

.input-hint {
  font-size: 10px;
  color: var(--text-placeholder, #5A5A6E);
  margin-top: 4px;
}

/* 移动端 */
@media (max-width: 768px) {
  .ai-chat-panel { width: 100%; min-width: 100%; position: absolute; right: 0; top: 0; bottom: 0; z-index: 100; }
  .ai-chat-panel.collapsed { width: 0; min-width: 0; }
}
</style>
