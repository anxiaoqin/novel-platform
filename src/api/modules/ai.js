/**
 * AI模块API
 * 包含AI写作、去AI味、纠错、分析等功能
 */

import api from '../index'

/**
 * 通用AI生成
 */
export function aiGenerate(data) {
  return api.post('/ai/generate', data)
}

/**
 * AI写作（指定模式）
 */
export function aiWrite(data) {
  return api.post('/ai/write', data)
}

/**
 * 应用AI写作结果
 */
export function applyAiWrite(data) {
  return api.post('/ai/write/apply', data)
}

/**
 * AI对话
 */
export function aiChat(data) {
  return api.post('/ai/chat', data)
}

// ==================== 纠错模块 ====================

/**
 * 基础AI纠错
 */
export function proofread(data) {
  return api.post('/ai/proofread', data)
}

/**
 * 网文专属6维纠错
 */
export function novelCheck(data) {
  return api.post('/ai/novel-check', data)
}

/**
 * 获取6维检查维度说明
 */
export function getNovelCheckDimensions() {
  return api.get('/ai/novel-check/dimensions')
}

/**
 * 前端兼容路径纠错
 */
export function checkErrors(data) {
  return api.post('/ai/check-errors', data)
}

// ==================== 分析模块 ====================

/**
 * AI章节分析
 */
export function analyzeChapter(data) {
  return api.post('/ai/analyze-chapter', data)
}

/**
 * 分析段落提取元素
 */
export function analyzeParagraph(data) {
  return api.post('/ai/analyze-paragraph', data)
}

// ==================== 填充模块 ====================

/**
 * 根据事件大纲填充章节
 */
export function fillChapter(data) {
  return api.post('/ai/fill-chapter', data)
}

/**
 * 单事件独立填充
 */
export function fillEvent(data) {
  return api.post('/ai/fill-event', data)
}

/**
 * 多候选填充
 */
export function fillChapterMulti(data) {
  return api.post('/ai/fill-chapter/multi', data)
}

// ==================== 续写模块 ====================

/**
 * 智能续写
 */
export function continueWriting(data) {
  return api.post('/ai/continue-writing', data)
}

// ==================== 去AI味模块 ====================

/**
 * AI味检测
 */
export function deaiDetect(data) {
  return api.post('/ai/deai-detect', data)
}

/**
 * 去AI味改写
 */
export function deaiRewrite(data) {
  return api.post('/ai/deai-rewrite', data)
}

// ==================== 大纲模块 ====================

/**
 * 保存章节事件大纲
 */
export function saveOutlineEvents(data) {
  return api.post('/ai/save-outline-events', data)
}

/**
 * 创建大纲
 */
export function createOutline(data) {
  return api.post('/ai/create-outline', data)
}

/**
 * 更新大纲
 */
export function updateOutline(data) {
  return api.post('/ai/update-outline', data)
}

// ==================== 知识库模块 ====================

/**
 * 事实知识检索
 */
export function knowledgeSearch(data) {
  return api.post('/ai/knowledge-search', data)
}

// ==================== 时间线AI ====================

/**
 * 生成时间线
 */
export function generateTimeline(data) {
  return api.post('/ai/timeline/generate', data)
}

/**
 * 应用时间线
 */
export function applyTimeline(data) {
  return api.post('/ai/timeline/apply', data)
}

// ==================== AI标签 ====================

/**
 * 生成标签
 */
export function generateTags(data) {
  return api.post('/ai/tags/generate', data)
}

/**
 * 保存标签
 */
export function saveTags(data) {
  return api.post('/ai/tags/save', data)
}

/**
 * 获取热门标签
 */
export function getPopularTags() {
  return api.get('/ai/tags/popular')
}

// ==================== 创作框架 ====================

/**
 * 创建创作框架
 */
export function createFramework(data) {
  return api.post('/ai/create-framework', data)
}

/**
 * 更新创作框架
 */
export function updateFramework(data) {
  return api.post('/ai/update-framework', data)
}

// ==================== 写作DNA ====================

/**
 * 分析写作风格
 */
export function analyzeWritingDNA(data) {
  return api.post('/ai/writing-dna/analyze', data)
}

export default {
  // 通用
  aiGenerate,
  aiWrite,
  applyAiWrite,
  aiChat,
  
  // 纠错
  proofread,
  novelCheck,
  getNovelCheckDimensions,
  checkErrors,
  
  // 分析
  analyzeChapter,
  analyzeParagraph,
  
  // 填充
  fillChapter,
  fillEvent,
  fillChapterMulti,
  
  // 续写
  continueWriting,
  
  // 去AI味
  deaiDetect,
  deaiRewrite,
  
  // 大纲
  saveOutlineEvents,
  createOutline,
  updateOutline,
  
  // 知识库
  knowledgeSearch,
  
  // 时间线
  generateTimeline,
  applyTimeline,
  
  // 标签
  generateTags,
  saveTags,
  getPopularTags,
  
  // 框架
  createFramework,
  updateFramework,
  
  // 写作DNA
  analyzeWritingDNA
}
