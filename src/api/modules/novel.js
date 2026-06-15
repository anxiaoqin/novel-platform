/**
 * 作品模块 (Novel)
 * 处理小说作品 CRUD 操作及统计
 */

import api from '../index'

/**
 * 获取作品列表
 * @param {object} [params] - 查询参数
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.status] - 状态过滤
 * @param {string} [params.keyword] - 关键词搜索
 * @returns {Promise<{list: array, total: number}>} 作品列表
 */
export function getNovels(params) {
  return api.get('/novels', { params })
}

/**
 * 创建新作品
 * @param {object} data - 作品信息
 * @param {string} data.title - 书名
 * @param {string} [data.description] - 简介
 * @param {string} [data.genre] - 类型/题材
 * @param {string} [data.tags] - 标签
 * @returns {Promise<object>} 创建的作品信息
 */
export function createNovel(data) {
  return api.post('/novels', data)
}

/**
 * 获取作品详情
 * @param {number} id - 作品ID
 * @returns {Promise<object>} 作品详情
 */
export function getNovel(id) {
  return api.get(`/novels/${id}`)
}

/**
 * 更新作品信息
 * @param {number} id - 作品ID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的作品信息
 */
export function updateNovel(id, data) {
  return api.put(`/novels/${id}`, data)
}

/**
 * 删除作品
 * @param {number} id - 作品ID
 * @returns {Promise<void>}
 */
export function deleteNovel(id) {
  return api.delete(`/novels/${id}`)
}

/**
 * 获取作品统计
 * @param {number} id - 作品ID
 * @returns {Promise<object>} 作品统计数据
 */
export function getNovelStats(id) {
  return api.get(`/novels/${id}/stats`)
}
