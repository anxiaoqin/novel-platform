/**
 * SSE 流式请求工具
 * 支持 Server-Sent Events 流式响应
 */

import api from './index'

/**
 * SSE 流式请求函数
 * @param {string} url - 请求URL（不含baseURL部分）
 * @param {object} body - 请求体数据
 * @param {object} options - 配置选项
 * @param {function} options.onMessage - 消息回调，接收解析后的数据
 * @param {function} options.onDone - 完成回调
 * @param {function} options.onError - 错误回调
 * @param {function} options.onProgress - 进度回调
 * @returns {AbortController} 用于取消请求的控制器
 */
export function createSSEStream(url, body, options = {}) {
  const { onMessage, onDone, onError, onProgress } = options
  
  const controller = new AbortController()
  const token = localStorage.getItem('token')
  
  const fetchUrl = `${api.defaults.baseURL}${url}`
  
  fetch(fetchUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'Accept': 'text/event-stream',
      'Cache-Control': 'no-cache'
    },
    body: JSON.stringify(body),
    signal: controller.signal
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let totalLength = 0
      
      function read() {
        reader.read().then(({ done, value }) => {
          if (done) {
            // 处理缓冲区中剩余的数据
            if (buffer.trim()) {
              processBuffer(buffer, onMessage, onProgress)
            }
            onDone?.()
            return
          }
          
          totalLength += value.length
          buffer += decoder.decode(value, { stream: true })
          
          // 按行分割处理
          const lines = buffer.split('\n')
          buffer = lines.pop() || '' // 保留最后一行（可能不完整）
          
          for (const line of lines) {
            processLine(line, onMessage, onProgress)
          }
          
          read()
        }).catch(error => {
          if (error.name !== 'AbortError') {
            onError?.(error)
          }
        })
      }
      
      read()
    })
    .catch(error => {
      if (error.name !== 'AbortError') {
        onError?.(error)
      }
    })
  
  return controller
}

/**
 * 处理单行 SSE 数据
 * @param {string} line - SSE 行数据
 * @param {function} onMessage - 消息回调
 * @param {function} onProgress - 进度回调
 */
function processLine(line, onMessage, onProgress) {
  if (!line.startsWith('data: ')) return
  
  const data = line.slice(6).trim()
  
  // 处理 [DONE] 结束信号
  if (data === '[DONE]') {
    return
  }
  
  // 尝试解析 JSON
  try {
    const parsed = JSON.parse(data)
    onMessage?.(parsed)
    
    // 提取进度信息
    if (parsed.choices?.[0]?.finish_reason === 'stop') {
      onProgress?.(100)
    }
  } catch (e) {
    // 如果不是完整 JSON，可能包含增量内容
    if (data) {
      onMessage?.({ type: 'text', content: data })
    }
  }
}

/**
 * 处理缓冲区数据
 * @param {string} buffer - 缓冲区数据
 * @param {function} onMessage - 消息回调
 * @param {function} onProgress - 进度回调
 */
function processBuffer(buffer, onMessage, onProgress) {
  const lines = buffer.split('\n')
  for (const line of lines) {
    processLine(line, onMessage, onProgress)
  }
}

/**
 * 解析 SSE 响应中的 content
 * @param {object} data - SSE 数据对象
 * @returns {string|null} 提取的文本内容
 */
export function extractContent(data) {
  // OpenAI 格式
  if (data.choices?.[0]?.delta?.content) {
    return data.choices[0].delta.content
  }
  // 自定义格式
  if (data.content) {
    return data.content
  }
  // 嵌套格式
  if (data.choices?.[0]?.delta?.content) {
    return data.choices[0].delta.content
  }
  return null
}

/**
 * 解析 SSE 增量数据
 * @param {object} data - SSE 数据对象
 * @returns {object} 解析后的增量数据
 */
export function parseDelta(data) {
  return {
    content: extractContent(data),
    role: data.choices?.[0]?.delta?.role || data.role,
    finishReason: data.choices?.[0]?.finish_reason || data.finish_reason,
    raw: data
  }
}

// ============ Vue Composable ============

/**
 * SSE Composable - 在 Vue 组件中使用
 * @param {string} url - 请求URL
 * @param {object} body - 请求体
 * @param {object} options - 配置选项
 * @returns {object} SSE 控制对象
 */
export function useSSE(url, body, options = {}) {
  const {
    onMessage = () => {},
    onDone = () => {},
    onError = () => {},
    immediate = false
  } = options
  
  const isStreaming = ref(false)
  const error = ref(null)
  const controller = ref(null)
  const accumulatedContent = ref('')
  
  /**
   * 开始流式请求
   */
  function start() {
    if (isStreaming.value) return
    
    isStreaming.value = true
    error.value = null
    accumulatedContent.value = ''
    
    controller.value = createSSEStream(url, body, {
      onMessage: (data) => {
        const content = extractContent(data)
        if (content) {
          accumulatedContent.value += content
        }
        onMessage(data, accumulatedContent.value)
      },
      onDone: () => {
        isStreaming.value = false
        onDone(accumulatedContent.value)
      },
      onError: (err) => {
        isStreaming.value = false
        error.value = err
        onError(err)
      }
    })
  }
  
  /**
   * 停止流式请求
   */
  function stop() {
    if (controller.value) {
      controller.value.abort()
      controller.value = null
    }
    isStreaming.value = false
  }
  
  /**
   * 重启流式请求
   */
  function restart() {
    stop()
    start()
  }
  
  // 立即执行
  if (immediate) {
    start()
  }
  
  // 组件卸载时自动停止
  onUnmounted(() => {
    stop()
  })
  
  return {
    isStreaming: readonly(isStreaming),
    error: readonly(error),
    accumulatedContent: readonly(accumulatedContent),
    start,
    stop,
    restart
  }
}

// 从 Vue 导入（在 <script setup> 中使用时自动可用）
import { ref, readonly, onUnmounted } from 'vue'

// ============ 预设的流式请求方法 ============

/**
 * 章节续写流式请求
 * @param {object} data - 请求数据
 * @param {function} onMessage - 消息回调
 * @param {function} onDone - 完成回调
 * @param {function} onError - 错误回调
 * @returns {AbortController}
 */
export function fillChapterStream(data, { onMessage, onDone, onError } = {}) {
  return createSSEStream('/ai/fill-chapter/stream', data, { onMessage, onDone, onError })
}

/**
 * 继续写作流式请求
 * @param {object} data - 请求数据
 * @param {function} onMessage - 消息回调
 * @param {function} onDone - 完成回调
 * @param {function} onError - 错误回调
 * @returns {AbortController}
 */
export function continueWritingStream(data, { onMessage, onDone, onError } = {}) {
  return createSSEStream('/ai/continue-writing/stream', data, { onMessage, onDone, onError })
}

/**
 * 去AI化改写流式请求
 * @param {object} data - 请求数据
 * @param {function} onMessage - 消息回调
 * @param {function} onDone - 完成回调
 * @param {function} onError - 错误回调
 * @returns {AbortController}
 */
export function deaiRewriteStream(data, { onMessage, onDone, onError } = {}) {
  return createSSEStream('/ai/deai-rewrite/stream', data, { onMessage, onDone, onError })
}

/**
 * 段落分析流式请求
 * @param {object} data - 请求数据
 * @param {function} onMessage - 消息回调
 * @param {function} onDone - 完成回调
 * @param {function} onError - 错误回调
 * @returns {AbortController}
 */
export function analyzeParagraphStream(data, { onMessage, onDone, onError } = {}) {
  return createSSEStream('/ai/analyze-paragraph/stream', data, { onMessage, onDone, onError })
}

/**
 * AI 对话流式请求
 * @param {object} data - 请求数据
 * @param {function} onMessage - 消息回调
 * @param {function} onDone - 完成回调
 * @param {function} onError - 错误回调
 * @returns {AbortController}
 */
export function chatStream(data, { onMessage, onDone, onError } = {}) {
  return createSSEStream('/ai/chat/stream', data, { onMessage, onDone, onError })
}

export default {
  createSSEStream,
  extractContent,
  parseDelta,
  useSSE,
  fillChapterStream,
  continueWritingStream,
  deaiRewriteStream,
  analyzeParagraphStream,
  chatStream
}
