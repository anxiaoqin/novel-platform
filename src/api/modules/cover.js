/**
 * 封面模块 (Cover)
 * 处理作品封面获取、生成、上传
 */

import api from '../index'

/**
 * 获取作品封面
 * @param {number} novelId - 作品ID
 * @returns {Promise<object>} 封面信息
 */
export function getCover(novelId) {
  return api.get(`/covers/${novelId}`)
}

/**
 * AI 生成封面
 * @param {number} novelId - 作品ID
 * @param {object} data - 生成参数
 * @param {string} [data.style] - 风格
 * @param {string} [data.prompt] - 提示词
 * @param {string} [data.description] - 作品描述
 * @returns {Promise<object>} 生成的封面
 */
export function generateCover(novelId, data) {
  return api.post(`/covers/${novelId}/generate`, data)
}

/**
 * 上传封面
 * @param {number} novelId - 作品ID
 * @param {object} data - 上传数据
 * @param {string} data.url - 封面URL
 * @returns {Promise<object>} 上传结果
 */
export function uploadCover(novelId, data) {
  return api.post(`/covers/${novelId}/upload`, data)
}
