/**
 * 积分模块 (Credits)
 * 处理积分余额、积分记录、签到等接口
 */

import api from '../index'

/**
 * 获取积分余额
 * @returns {Promise<{balance: number}>} 当前积分余额
 */
export function getBalance() {
  return api.get('/credits/balance')
}

/**
 * 获取积分历史记录
 * @param {object} [params] - 查询参数
 * @param {number} [params.page] - 页码
 * @param {number} [params.pageSize] - 每页数量
 * @param {string} [params.type] - 类型过滤 (earn/spend)
 * @returns {Promise<{list: array, total: number}>} 积分记录列表
 */
export function getHistory(params) {
  return api.get('/credits/history', { params })
}

/**
 * 每日签到
 * @returns {Promise<{credits: number, consecutiveDays: number}>} 签到结果
 */
export function signin() {
  return api.post('/credits/signin')
}

/**
 * 获取每日积分使用情况
 * @param {string} [date] - 日期 (YYYY-MM-DD格式)
 * @returns {Promise<object>} 每日使用统计
 */
export function getDailyUsage(date) {
  return api.get('/credits/usage/daily', { params: { date } })
}
