/**
 * 大纲模块 (Outline)
 * 处理小说大纲版本管理
 */

import api from '../index'

/**
 * 获取大纲树
 * @param {number} novelId - 作品ID
 * @returns {Promise<object>} 大纲树结构
 */
export function getOutlineTree(novelId) {
  return api.get(`/novels/${novelId}/outline-tree`)
}

/**
 * 获取大纲版本列表
 * @param {number} novelId - 作品ID
 * @returns {Promise<array>} 版本列表
 */
export function getOutlineVersions(novelId) {
  return api.get(`/novels/${novelId}/outline-versions`)
}

/**
 * 保存大纲版本
 * @param {number} novelId - 作品ID
 * @param {object} data - 大纲数据
 * @param {object} data.content - 大纲内容
 * @param {string} [data.description] - 版本描述
 * @returns {Promise<object>} 保存的版本
 */
export function saveOutlineVersion(novelId, data) {
  return api.post(`/novels/${novelId}/outline-versions`, data)
}

/**
 * 激活大纲版本
 * @param {number} novelId - 作品ID
 * @param {number} vid - 版本ID
 * @returns {Promise<object>} 激活结果
 */
export function activateOutlineVersion(novelId, vid) {
  return api.put(`/novels/${novelId}/outline-versions/${vid}/activate`)
}

/**
 * 删除大纲版本
 * @param {number} novelId - 作品ID
 * @param {number} vid - 版本ID
 * @returns {Promise<void>}
 */
export function deleteOutlineVersion(novelId, vid) {
  return api.delete(`/novels/${novelId}/outline-versions/${vid}`)
}
