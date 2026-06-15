/**
 * 流式模块 (Stream)
 * 处理所有 SSE 流式接口
 * 注意：这些接口使用 fetch 实现，不依赖 axios
 */

import { createSSEStream } from '../sse'

/**
 * 章节填充流式请求
 * @param {object} data - 请求参数
 * @param {number} data.novelId - 作品ID
 * @param {number} [data.chapterId] - 章节ID
 * @param {string} data.outline - 大纲内容
 * @param {object} callbacks - 回调函数
 * @param {function} callbacks.onMessage - 消息回调
 * @param {function} callbacks.onDone - 完成回调
 * @param {function} callbacks.onError - 错误回调
 * @param {function} callbacks.onProgress - 进度回调
 * @returns {AbortController}
 */
export function fillChapterStream(data, callbacks = {}) {
  return createSSEStream('/ai/fill-chapter/stream', data, callbacks)
}

/**
 * 继续写作流式请求
 * @param {object} data - 请求参数
 * @param {number} data.chapterId - 章节ID
 * @param {string} data.content - 当前内容
 * @param {object} callbacks - 回调函数
 * @returns {AbortController}
 */
export function continueWritingStream(data, callbacks = {}) {
  return createSSEStream('/ai/continue-writing/stream', data, callbacks)
}

/**
 * 去AI化改写流式请求
 * @param {object} data - 请求参数
 * @param {string} data.text - 待改写文本
 * @param {string} [data.style] - 目标风格
 * @param {object} callbacks - 回调函数
 * @returns {AbortController}
 */
export function deaiRewriteStream(data, callbacks = {}) {
  return createSSEStream('/ai/deai-rewrite/stream', data, callbacks)
}

/**
 * 段落分析流式请求
 * @param {object} data - 请求参数
 * @param {string} data.content - 段落内容
 * @param {number} [data.novelId] - 作品ID
 * @param {number} [data.chapterId] - 章节ID
 * @param {object} callbacks - 回调函数
 * @returns {AbortController}
 */
export function analyzeParagraphStream(data, callbacks = {}) {
  return createSSEStream('/ai/analyze-paragraph/stream', data, callbacks)
}
