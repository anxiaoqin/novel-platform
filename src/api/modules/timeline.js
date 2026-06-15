/**
 * 时间线模块 (Timeline)
 * 处理作品时间线 CRUD 操作
 */

import api from '../index'

/**
 * 获取作品时间线
 * @param {number} novelId - 作品ID
 * @returns {Promise<array>} 时间线列表
 */
export function getTimelines(novelId) {
  return api.get(`/novels/${novelId}/timelines`)
}

/**
 * 创建时间线节点
 * @param {number} novelId - 作品ID
 * @param {object} data - 时间线信息
 * @param {string} data.title - 标题
 * @param {string} [data.description] - 描述
 * @param {string} [data.startTime] - 开始时间
 * @param {string} [data.endTime] - 结束时间
 * @param {string} [data.type] - 类型
 * @param {array} [data.characters] - 关联角色
 * @returns {Promise<object>} 创建的时间线节点
 */
export function createTimeline(novelId, data) {
  return api.post(`/novels/${novelId}/timelines`, data)
}

/**
 * 更新时间线节点
 * @param {number} novelId - 作品ID
 * @param {number} timelineId - 时间线ID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的时间线节点
 */
export function updateTimeline(novelId, timelineId, data) {
  return api.put(`/novels/${novelId}/timelines/${timelineId}`, data)
}

/**
 * 删除时间线节点
 * @param {number} novelId - 作品ID
 * @param {number} timelineId - 时间线ID
 * @returns {Promise<void>}
 */
export function deleteTimeline(novelId, timelineId) {
  return api.delete(`/novels/${novelId}/timelines/${timelineId}`)
}
