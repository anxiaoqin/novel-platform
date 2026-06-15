/**
 * 章节版本模块 (ChapterVersion)
 * 处理章节版本历史管理
 */

import api from '../index'

/**
 * 获取章节版本列表
 * @param {number} chapterId - 章节ID
 * @param {object} [params] - 查询参数
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @returns {Promise<{list: array, total: number}>} 版本列表
 */
export function getChapterVersions(chapterId, params) {
  return api.get(`/chapters/${chapterId}/versions`, { params })
}

/**
 * 保存章节版本快照
 * @param {number} chapterId - 章节ID
 * @param {object} data - 版本数据
 * @param {string} data.content - 章节内容
 * @param {string} [data.description] - 版本描述
 * @returns {Promise<object>} 保存的版本
 */
export function saveChapterVersion(chapterId, data) {
  return api.post(`/chapters/${chapterId}/versions`, data)
}

/**
 * 获取版本详情
 * @param {number} versionId - 版本ID
 * @returns {Promise<object>} 版本详情
 */
export function getChapterVersion(versionId) {
  return api.get(`/chapter-versions/${versionId}`)
}

/**
 * 恢复章节版本
 * @param {number} versionId - 版本ID
 * @returns {Promise<object>} 恢复结果
 */
export function restoreChapterVersion(versionId) {
  return api.put(`/chapter-versions/${versionId}/restore`)
}

/**
 * 删除章节版本
 * @param {number} versionId - 版本ID
 * @returns {Promise<void>}
 */
export function deleteChapterVersion(versionId) {
  return api.delete(`/chapter-versions/${versionId}`)
}

/**
 * 对比两个版本差异
 * @param {number} v1Id - 版本1 ID
 * @param {number} v2Id - 版本2 ID
 * @returns {Promise<object>} 差异结果
 */
export function diffChapterVersions(v1Id, v2Id) {
  return api.get(`/chapter-versions/${v1Id}/diff/${v2Id}`)
}
