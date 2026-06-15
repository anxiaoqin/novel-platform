/**
 * 其他模块 (Other)
 * 处理物品卡牌、写作上下文、法律文档、草稿、帖子等接口
 */

import api from '../index'

// ============ 物品卡牌 ============

/**
 * 获取物品卡牌列表
 * @param {number} novelId - 作品ID
 * @returns {Promise<array>} 物品卡牌列表
 */
export function getItemCards(novelId) {
  return api.get(`/novels/${novelId}/item-cards`)
}

/**
 * 创建物品卡牌
 * @param {number} novelId - 作品ID
 * @param {object} data - 卡牌数据
 * @param {string} data.name - 物品名称
 * @param {string} [data.type] - 物品类型
 * @param {string} [data.description] - 描述
 * @param {object} [data.attributes] - 属性
 * @returns {Promise<object>} 创建的卡牌
 */
export function createItemCard(novelId, data) {
  return api.post(`/novels/${novelId}/item-cards`, data)
}

/**
 * 更新物品卡牌
 * @param {number} id - 卡牌ID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的卡牌
 */
export function updateItemCard(id, data) {
  return api.put(`/item-cards/${id}`, data)
}

/**
 * 删除物品卡牌
 * @param {number} id - 卡牌ID
 * @returns {Promise<void>}
 */
export function deleteItemCard(id) {
  return api.delete(`/item-cards/${id}`)
}

// ============ 写作上下文 ============

/**
 * 获取写作上下文
 * @param {number} novelId - 作品ID
 * @param {number} chapterId - 章节ID
 * @returns {Promise<object>} 写作上下文
 */
export function getWritingContext(novelId, chapterId) {
  return api.get(`/novels/${novelId}/writing-context/${chapterId}`)
}

// ============ 法律文档 ============

/**
 * 获取法律文档
 * @param {string} docType - 文档类型 (privacy/terms)
 * @returns {Promise<object>} 文档内容
 */
export function getLegalDoc(docType) {
  return api.get(`/legal/${docType}`)
}

/**
 * 获取法律文档列表
 * @returns {Promise<array>} 文档列表
 */
export function getLegalList() {
  return api.get('/legal/list')
}

/**
 * 接受法律协议
 * @param {object} data - 接受数据
 * @param {string} data.docType - 文档类型
 * @param {boolean} data.accepted - 是否接受
 * @returns {Promise<object>} 接受结果
 */
export function acceptLegal(data) {
  return api.post('/legal/accept', data)
}

/**
 * 获取法律协议接受状态
 * @returns {Promise<object>} 接受状态
 */
export function getLegalAcceptanceStatus() {
  return api.get('/legal/acceptance-status')
}

// ============ 草稿 ============

/**
 * 获取草稿列表
 * @param {object} [params] - 查询参数
 * @returns {Promise<{list: array, total: number}>} 草稿列表
 */
export function getDrafts(params) {
  return api.get('/drafts', { params })
}

/**
 * 创建草稿
 * @param {object} data - 草稿数据
 * @param {string} data.title - 标题
 * @param {string} [data.content] - 内容
 * @param {number} [data.novelId] - 关联作品ID
 * @returns {Promise<object>} 创建的草稿
 */
export function createDraft(data) {
  return api.post('/drafts', data)
}

/**
 * 获取草稿详情
 * @param {number} id - 草稿ID
 * @returns {Promise<object>} 草稿详情
 */
export function getDraft(id) {
  return api.get(`/drafts/${id}`)
}

/**
 * 更新草稿
 * @param {number} id - 草稿ID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的草稿
 */
export function updateDraft(id, data) {
  return api.put(`/drafts/${id}`, data)
}

/**
 * 删除草稿
 * @param {number} id - 草稿ID
 * @returns {Promise<void>}
 */
export function deleteDraft(id) {
  return api.delete(`/drafts/${id}`)
}

// ============ 帖子 ============

/**
 * 获取帖子列表
 * @param {object} [params] - 查询参数
 * @returns {Promise<{list: array, total: number}>} 帖子列表
 */
export function getPosts(params) {
  return api.get('/posts', { params })
}

/**
 * 创建帖子
 * @param {object} data - 帖子数据
 * @param {string} data.title - 标题
 * @param {string} data.content - 内容
 * @param {string} [data.type] - 帖子类型
 * @returns {Promise<object>} 创建的帖子
 */
export function createPost(data) {
  return api.post('/posts', data)
}

/**
 * 获取帖子详情
 * @param {number} id - 帖子ID
 * @returns {Promise<object>} 帖子详情
 */
export function getPost(id) {
  return api.get(`/posts/${id}`)
}

/**
 * 删除帖子
 * @param {number} id - 帖子ID
 * @returns {Promise<void>}
 */
export function deletePost(id) {
  return api.delete(`/posts/${id}`)
}

/**
 * 点赞帖子
 * @param {number} id - 帖子ID
 * @returns {Promise<object>} 点赞结果
 */
export function likePost(id) {
  return api.post(`/posts/${id}/like`)
}

/**
 * 评论帖子
 * @param {number} id - 帖子ID
 * @param {object} data - 评论数据
 * @param {string} data.content - 评论内容
 * @returns {Promise<object>} 评论结果
 */
export function commentPost(id, data) {
  return api.post(`/posts/${id}/comments`, data)
}

// ============ 公开接口 ============

/**
 * 获取公开作品列表
 * @param {object} [params] - 查询参数
 * @returns {Promise<{list: array, total: number}>} 作品列表
 */
export function getPublicNovels(params) {
  return api.get('/public/novels', { params })
}

/**
 * 获取公开作品详情
 * @param {number} id - 作品ID
 * @returns {Promise<object>} 作品详情
 */
export function getPublicNovel(id) {
  return api.get(`/public/novels/${id}`)
}

/**
 * 获取公开排行榜
 * @param {object} [params] - 查询参数
 * @param {string} [params.type] - 排行榜类型
 * @returns {Promise<array>} 排行榜数据
 */
export function getPublicRank(params) {
  return api.get('/public/rank', { params })
}

// ============ 统计 ============

/**
 * 获取统计仪表盘
 * @returns {Promise<object>} 统计数据
 */
export function getStatsDashboard() {
  return api.get('/stats/dashboard')
}
