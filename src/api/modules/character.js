/**
 * 角色模块 (Character)
 * 处理角色设定、关系、成长线等接口
 */

import api from '../index'

/**
 * 获取作品角色列表
 * @param {number} novelId - 作品ID
 * @param {object} [params] - 查询参数
 * @param {string} [params.type] - 角色类型过滤
 * @returns {Promise<array>} 角色列表
 */
export function getCharacters(novelId, params) {
  return api.get(`/novels/${novelId}/characters`, { params })
}

/**
 * 创建角色
 * @param {number} novelId - 作品ID
 * @param {object} data - 角色信息
 * @param {string} data.name - 角色名
 * @param {string} [data.type] - 角色类型
 * @param {string} [data.description] - 角色描述
 * @param {object} [data.attributes] - 角色属性
 * @returns {Promise<object>} 创建的角色
 */
export function createCharacter(novelId, data) {
  return api.post(`/novels/${novelId}/characters`, data)
}

/**
 * 获取角色详情
 * @param {number} novelId - 作品ID
 * @param {number} charId - 角色ID
 * @returns {Promise<object>} 角色详情
 */
export function getCharacter(novelId, charId) {
  return api.get(`/novels/${novelId}/characters/${charId}`)
}

/**
 * 更新角色
 * @param {number} novelId - 作品ID
 * @param {number} charId - 角色ID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的角色
 */
export function updateCharacter(novelId, charId, data) {
  return api.put(`/novels/${novelId}/characters/${charId}`, data)
}

/**
 * 删除角色
 * @param {number} novelId - 作品ID
 * @param {number} charId - 角色ID
 * @returns {Promise<void>}
 */
export function deleteCharacter(novelId, charId) {
  return api.delete(`/novels/${novelId}/characters/${charId}`)
}

/**
 * 获取角色关系图
 * @param {number} novelId - 作品ID
 * @returns {Promise<array>} 角色关系列表
 */
export function getCharacterRelationships(novelId) {
  return api.get(`/novels/${novelId}/character-relationships`)
}

/**
 * 更新角色关系
 * @param {number} charId - 角色ID
 * @param {object} data - 关系数据
 * @param {array} [data.relationships] - 关系列表
 * @returns {Promise<object>} 更新结果
 */
export function updateRelationships(charId, data) {
  return api.put(`/characters/${charId}/relationships`, data)
}

/**
 * 更新角色成长线
 * @param {number} charId - 角色ID
 * @param {object} data - 成长线数据
 * @param {array} [data.growthLine] - 成长线事件
 * @returns {Promise<object>} 更新结果
 */
export function updateGrowthLine(charId, data) {
  return api.put(`/characters/${charId}/growth-line`, data)
}

/**
 * 批量查询角色
 * @param {number} novelId - 作品ID
 * @param {array<number>} ids - 角色ID数组
 * @returns {Promise<array>} 角色列表
 */
export function batchQueryCharacters(novelId, ids) {
  return api.post(`/novels/${novelId}/characters/batch-query`, { ids })
}
