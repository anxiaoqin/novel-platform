/**
 * 发布模块 (Publish)
 * 处理平台账号管理、作品发布等接口
 */

import api from '../index'

// ============ 平台账号 ============

/**
 * 获取平台账号列表
 * @returns {Promise<array>} 账号列表
 */
export function getPlatformAccounts() {
  return api.get('/platforms/accounts')
}

/**
 * 添加平台账号
 * @param {object} data - 账号数据
 * @param {string} data.platform - 平台名称
 * @param {string} data.username - 用户名
 * @param {string} [data.token] - 认证Token
 * @returns {Promise<object>} 添加的账号
 */
export function addPlatformAccount(data) {
  return api.post('/platforms/accounts', data)
}

/**
 * 删除平台账号
 * @param {number} accountId - 账号ID
 * @returns {Promise<void>}
 */
export function deletePlatformAccount(accountId) {
  return api.delete(`/platforms/accounts/${accountId}`)
}

/**
 * 验证平台账号
 * @param {number} accountId - 账号ID
 * @returns {Promise<object>} 验证结果
 */
export function verifyPlatformAccount(accountId) {
  return api.post(`/platforms/accounts/${accountId}/verify`)
}

// ============ 发布 ============

/**
 * 预览发布效果
 * @param {number} novelId - 作品ID
 * @returns {Promise<object>} 预览数据
 */
export function previewPublish(novelId) {
  return api.get(`/publish/preview/${novelId}`)
}

/**
 * 发布作品
 * @param {number} novelId - 作品ID
 * @param {object} [data] - 发布参数
 * @param {array} [data.accounts] - 目标平台账号
 * @returns {Promise<object>} 发布结果
 */
export function publishNovel(novelId, data) {
  return api.post(`/publish/${novelId}`, data)
}

/**
 * 获取发布记录
 * @param {object} [params] - 查询参数
 * @returns {Promise<{list: array, total: number}>} 发布记录
 */
export function getPublishRecords(params) {
  return api.get('/publish/records', { params })
}

/**
 * 获取发布记录详情
 * @param {number} recordId - 记录ID
 * @returns {Promise<object>} 记录详情
 */
export function getPublishRecord(recordId) {
  return api.get(`/publish/records/${recordId}`)
}

/**
 * 检测作品重复
 * @param {number} novelId - 作品ID
 * @returns {Promise<object>} 检测结果
 */
export function checkDuplicate(novelId) {
  return api.get(`/publish/check-duplicate/${novelId}`)
}

/**
 * 同步发布状态
 * @param {number} recordId - 记录ID
 * @returns {Promise<object>} 同步结果
 */
export function syncPublishStatus(recordId) {
  return api.post(`/publish/sync-status/${recordId}`)
}

/**
 * 检测已有作品
 * @param {object} [data] - 检测参数
 * @returns {Promise<array>} 已有作品列表
 */
export function detectExisting(data) {
  return api.post('/publish/detect-existing', data)
}

// ============ 平台会话 ============

/**
 * 获取平台登录URL
 * @param {string} platform - 平台名称
 * @returns {Promise<{url: string}>} 登录URL
 */
export function getPlatformLoginUrl(platform) {
  return api.get(`/platforms/${platform}/login-url`)
}

/**
 * 保存平台会话
 * @param {string} platform - 平台名称
 * @param {object} data - 会话数据
 * @returns {Promise<object>} 保存结果
 */
export function savePlatformSession(platform, data) {
  return api.post(`/platforms/${platform}/save-session`, data)
}

/**
 * 检查平台会话
 * @param {string} platform - 平台名称
 * @returns {Promise<object>} 会话状态
 */
export function checkPlatformSession(platform) {
  return api.get(`/platforms/${platform}/check-session`)
}

/**
 * 加载平台会话
 * @param {string} platform - 平台名称
 * @returns {Promise<object>} 会话数据
 */
export function loadPlatformSession(platform) {
  return api.get(`/platforms/${platform}/load-session`)
}

// ============ 发布数据 ============

/**
 * 获取发布任务数据
 * @param {number} novelId - 作品ID
 * @returns {Promise<object>} 任务数据
 */
export function getPublishTaskData(novelId) {
  return api.get(`/publish/task-data/${novelId}`)
}

/**
 * 章节上报
 * @param {object} data - 上报数据
 * @returns {Promise<object>} 上报结果
 */
export function chapterReport(data) {
  return api.post('/publish/chapter-report', data)
}

/**
 * 书籍创建完成
 * @param {object} data - 书籍数据
 * @returns {Promise<object>} 创建结果
 */
export function bookCreated(data) {
  return api.post('/publish/book-created', data)
}

/**
 * 获取已有作品
 * @param {object} [params] - 查询参数
 * @returns {Promise<array>} 作品列表
 */
export function getExistingWorks(params) {
  return api.get('/publish/existing-works', { params })
}
