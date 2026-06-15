/**
 * 章节模块 (Chapter)
 * 处理小说章节 CRUD 操作
 */

import api from '../index'

/**
 * 获取作品章节列表
 * @param {number} novelId - 作品ID
 * @param {object} [params] - 查询参数
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.status] - 状态过滤
 * @returns {Promise<{list: array, total: number}>} 章节列表
 */
export function getChapters(novelId, params) {
  return api.get(`/novels/${novelId}/chapters`, { params })
}

/**
 * 创建新章节
 * @param {number} novelId - 作品ID
 * @param {object} data - 章节信息
 * @param {string} data.title - 章节标题
 * @param {number} [data.order] - 排序序号
 * @param {string} [data.content] - 章节内容
 * @returns {Promise<object>} 创建的章节信息
 */
export function createChapter(novelId, data) {
  return api.post(`/novels/${novelId}/chapters`, data)
}

/**
 * 获取章节详情
 * @param {number} id - 章节ID
 * @returns {Promise<object>} 章节详情
 */
export function getChapter(id) {
  return api.get(`/chapters/${id}`)
}

/**
 * 更新章节
 * @param {number} id - 章节ID
 * @param {object} data - 更新的数据
 * @param {string} [data.title] - 章节标题
 * @param {string} [data.content] - 章节内容
 * @param {number} [data.status] - 状态
 * @returns {Promise<object>} 更新后的章节
 */
export function updateChapter(id, data) {
  return api.put(`/chapters/${id}`, data)
}

/**
 * 删除章节
 * @param {number} id - 章节ID
 * @returns {Promise<void>}
 */
export function deleteChapter(id) {
  return api.delete(`/chapters/${id}`)
}
