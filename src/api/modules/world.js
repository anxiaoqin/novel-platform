/**
 * 世界观模块 (World)
 * 处理作品世界观设定 CRUD 操作
 */

import api from '../index'

/**
 * 获取作品世界观列表
 * @param {number} novelId - 作品ID
 * @returns {Promise<array>} 世界观列表
 */
export function getWorlds(novelId) {
  return api.get(`/novels/${novelId}/worlds`)
}

/**
 * 创建世界观设定
 * @param {number} novelId - 作品ID
 * @param {object} data - 世界观信息
 * @param {string} data.name - 名称
 * @param {string} [data.type] - 类型 (region/person/item/event)
 * @param {string} [data.description] - 描述
 * @param {object} [data.attributes] - 属性
 * @returns {Promise<object>} 创建的世界观信息
 */
export function createWorld(novelId, data) {
  return api.post(`/novels/${novelId}/worlds`, data)
}

/**
 * 获取世界观详情
 * @param {number} novelId - 作品ID
 * @param {number} worldId - 世界观ID
 * @returns {Promise<object>} 世界观详情
 */
export function getWorld(novelId, worldId) {
  return api.get(`/novels/${novelId}/worlds/${worldId}`)
}

/**
 * 更新世界观
 * @param {number} novelId - 作品ID
 * @param {number} worldId - 世界观ID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的世界观
 */
export function updateWorld(novelId, worldId, data) {
  return api.put(`/novels/${novelId}/worlds/${worldId}`, data)
}

/**
 * 删除世界观
 * @param {number} novelId - 作品ID
 * @param {number} worldId - 世界观ID
 * @returns {Promise<void>}
 */
export function deleteWorld(novelId, worldId) {
  return api.delete(`/novels/${novelId}/worlds/${worldId}`)
}
