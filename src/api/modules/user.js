/**
 * 用户模块 (User)
 * 处理用户信息、设置、积分、写作统计等接口
 */

import api from '../index'

/**
 * 获取用户设置
 * @returns {Promise<object>} 用户设置信息
 */
export function getSettings() {
  return api.get('/users/settings')
}

/**
 * 更新用户设置
 * @param {object} data - 设置数据
 * @param {string} [data.nickname] - 昵称
 * @param {string} [data.avatar] - 头像URL
 * @param {object} [data.preferences] - 偏好设置
 * @returns {Promise<object>} 更新后的设置信息
 */
export function updateSettings(data) {
  return api.put('/users/settings', data)
}

/**
 * 获取用户积分信息
 * @returns {Promise<{balance: number, total: number, signinDays: number}>} 积分信息
 */
export function getCredits() {
  return api.get('/users/credits')
}

/**
 * 获取用户写作统计
 * @returns {Promise<object>} 写作统计数据
 */
export function getWritingStats() {
  return api.get('/users/me/writing-stats')
}
